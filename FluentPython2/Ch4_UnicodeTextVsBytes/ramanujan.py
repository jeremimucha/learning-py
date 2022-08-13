#!/usr/bin/env python3

import re

re_numbers_str = re.compile(r'\d+')
re_words_str = re.compile(r'\w+')
re_numbers_bytes = re.compile(rb'\d+')
re_words_bytes = re.compile(rb'\w+')

text_str = ("Ramanujan saw \u0b37\u0bed\u0be8\u0bef"
            " as 1729 = 1³ + 12³ = 9³ + 10³.")

text_bytes = text_str.encode('utf-8')

print(f"Text\n, {text_str!r}")
print("Numbers")
print("  str  :", re_numbers_str.findall(text_str))
print("  bytes:", re_numbers_bytes.findall(text_bytes))
print("Words")
print("  str  :", re_words_str.findall(text_str))
print("  bytes:", re_words_bytes.findall(text_bytes))
