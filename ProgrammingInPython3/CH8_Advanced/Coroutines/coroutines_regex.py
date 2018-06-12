#! python3
import re


URL_RE = re.compile(r'''href=(?P<quote>['"])(?P<url>[^\1]+?)'''
                    r'''(?P=quote)''', re.IGNORECASE)
flags = re.MULTILINE | re.IGNORECASE | re.DOTALL
H1_RE = re.compile(r'<h1>(?P<h1>.+?)</h1>', flags)
H2_RE = re.compile(r'<h2>(?P<h2>.+?)</h2>', flags)


def coroutine(function):
    def wrapper(*args, **kwargs):
        generator = function(*args, **kwargs)
        next(generator)
        return generator
    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    return wrapper


@coroutine
def regex_matcher(receiver, regex):
    while True:
        text = (yield)
        for match in regex.finditer(text):
            receiver.send(match)

@coroutine
def reporter():
    ignore = frozenset({'style.css', 'favicon.png', 'index.html'})
    while True:
        match = (yield)
        if match is not None:
            try:
                groups = match.groupdict()
                if 'url' in groups and groups['url'] not in ignore:
                    print('   URL:', groups['url'])
                elif 'h1' in groups:
                    print('    H1:', groups['h1'])
                elif 'h2' in groups:
                    print('    H2:', groups['h2'])
            except UnicodeEncodeError: pass

receiver = reporter()
matchers = (regex_matcher(receiver, URL_RE),
            regex_matcher(receiver, H1_RE),
            regex_matcher(receiver, H2_RE))


if __name__ == '__main__':
    import sys
    try:
        for file in sys.argv[1:]:
            print(file)
            html = open(file, encoding='utf8').read()
            for matcher in matchers:
                matcher.send(html)
    finally:
        for matcher in matchers:
            matcher.close()
        receiver.close()
