#! python3
import re


phone_re = re.compile(r"""^[ \t]*
                      (?P<parenthesis>\()?
                      [- ]?
                      (?P<area>\d{3})
                      (?(parenthesis)\))
                      [- ]?
                      (?P<local_a>\d{3})
                      [- ]?
                      (?P<local_b>\d{4})
                      [ \t]*$
                        """, re.VERBOSE)


if __name__ == '__main__':
    print("US Phone number regex\n10 digits total\n3 digits area code\n"
        "7 digits local number. Hyphens and whitespace allowed.\n"
        "Parenthesised area code allowed.")
    while True:
        line = input('Enter a phone number: ')
        if not line:
            continue
        match = phone_re.match(line)
        if match:
            print("({0}) {1} {2}".format(match.group("area"),
                match.group("local_a"), match.group("local_b")))
        else:
            print("Invalid U.S phone number: {0}".format(line))
