import string


def is_ascii(s):
    '''
    >>> is_ascii('abcdefghijklmnoprstuwxyzABCDEFGHIJKLMNOPRSTUWXYZ')
    True
    '''
    return all( (ord(x) < 127 for x in s) )


def is_ascii_punctuation(s):
    '''
    >>> is_ascii_punctuation('.,!?')
    True
    '''
    return all( (x in string.punctuation for x in s) )


def is_ascii_printable(s:str) -> bool:
    '''
    assert is_ascii_printable('jklhasdoiuywer98235109')
    True
    '''
    return all( (x in string.printable for x in s) )


if __name__ == '__main__':
    import doctest
    doctest.testmod()
