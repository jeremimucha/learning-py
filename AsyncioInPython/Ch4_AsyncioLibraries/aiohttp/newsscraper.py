#! /usr/bin/env python

# Application demonstrating a use of aiohttp library to scrape news websites.

from asyncio import gather, create_task
from string import Template
from aiohttp import web, ClientSession
from bs4 import BeautifulSoup



def make_news(sites, splash_url):
    """:sites: is expected to be a list of tuples of (url, handler) of news sites.
    :splash_url: is the url of the Splash javascript rendering service.
    """
    async def news(request):
        # Create a task for each news website, fetching the data.
        tasks = [create_task(news_fetch(*s, splash_url=splash_url)) for s in sites]
        # gather all the tasks into a single future and await it immediately.
        await gather(*tasks)

        items = {
            text: (
                f'<div class="box {kind}">'
                f'<span>'
                f'<a href="{href}">{text}</a>'
                f'</span>'
                f'</div>'
            )
            for task in tasks for href, text, kind in task.result()
        }
        content = ''.join(items[x] for x in sorted(items))

        page = Template(open('index.html').read())
        return web.Response(
                    body=page.safe_substitute(body=content),
                    content_type='text/html'
                )
    return news

async def fixed_news(request):
        sites = [
            ('http://edition.cnn.com', cnn_articles),
            ('http://www.aljazeera.com', aljazeera_articles),
        ]
        # Create a task for each news website, fetching the data.
        tasks = [create_task(news_fetch(*s, splash_url='http://localhost:8050')) for s in sites]
        # gather all the tasks into a single future and await it immediately.
        await gather(*tasks)

        items = {
            text: (
                f'<div class="box {kind}">'
                f'<span>'
                f'<a href="{href}">{text}</a>'
                f'</span>'
                f'</div>'
            )
            for task in tasks for href, text, kind in task.result()
        }
        content = ''.join(items[x] for x in sorted(items))

        page = Template(open('index.html').read())
        print(page)
        return web.Response(
                    body=page.safe_substitute(body=content),
                    content_type='text/html'
                )


async def news_fetch(url, postprocess, splash_url):
    proxy_url = (
        f'{splash_url}/render.html?url={url}&timeout=60&wait=1'
    )
    # This is how the client API of the aiohttp can be used
    async with ClientSession() as session:
        async with session.get(proxy_url) as resp:
            data = await resp.read()
            data = data.decode('utf-8')
    return postprocess(url, data)


def cnn_articles(url, page_data):
    soup = BeautifulSoup(page_data, 'lxml')
    def match(tag):
        return (
            tag.text and tag.has_attr('href')
            and tag['href'].startswith('/')
            and tag['href'].endswith('.html')
            and tag.find(class_='cd__headline-text')
        )
    headlines = soup.find_all(match)
    return [(url + hl['href'], hl.text, 'cnn') for hl in headlines]


def aljazeera_articles(url, page_data):
    soup = BeautifulSoup(page_data, 'lxml')
    def match(tag):
        return (
            tag.text and tag.has_attr('href')
            and tag['href'].startswith('/news')
            and tag['href'].endswith('.html')
        )
    headlines = soup.find_all(match)
    return [(url + hl['href'], hl.text, 'aljazeera') for hl in headlines]


if __name__ == '__main__':
    from argparse import ArgumentParser
    cargs = ArgumentParser('News Scraper.')
    cargs.add_argument('--splash', help="url of the Splash javascript rendering service.",
                       default='http://localhost:8050')
    args = cargs.parse_args()

    sites = [
        ('http://edition.cnn.com', cnn_articles),
        ('http://www.aljazeera.com', aljazeera_articles),
    ]

    app = web.Application()
    app.router.add_get('/news', make_news(sites=sites, splash_url=args.splash))
    web.run_app(app, port=8080)
