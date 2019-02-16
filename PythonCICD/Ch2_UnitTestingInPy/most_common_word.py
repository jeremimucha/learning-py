#! python3

import requests

'''
This is bad and untestable. The function has multiple responsibilities.
There's no real way to have controll over the requests call by mocking it, etc.
'''

def most_common_word_in_web_page(words, url):
    '''
    finds the most common word from a list of words
    in a web page, identified by itd URL
    '''

    response = requests.get(url)
    text = response.text
    word_frequency = {w : text.count(w) for w in words}
    return sorted(word_frequency, key=word_frequency.get)[-1]


if __name__ == '__main__':
    most_common = most_common_word_in_web_page(['python', 'Python', 'programmin'],
        'https://python.org')
    print(most_common)
