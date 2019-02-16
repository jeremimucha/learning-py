#! python3
import requests


def most_common_word_in_webpage(words, url, req_agent=requests):
    response = req_agent.get(url)
    return most_common_word(words, response.text)

def most_common_word(words, text):
    word_frequency = {w : text.count(w) for w in words}
    return sorted(words, key=word_frequency.get)[-1]

if __name__ == '__main__':
    most_common = most_common_word_in_webpage(
        ['python', 'Python', 'programmin'],
        'https://python.org'
    )
    print(most_common)
