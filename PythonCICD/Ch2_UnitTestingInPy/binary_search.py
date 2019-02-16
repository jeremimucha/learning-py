#! python3

def search(needle, haystack):
    left = 0
    right = len(haystack) - 1

    while left <= right:
        middle = left + (right - left) // 2
        middle_elem = haystack[middle]
        if middle_elem == needle:
            return middle
        elif middle_elem < needle:
            left = middle + 1
        else:
            right = middle - 1
    raise ValueError("{} not in {}".format(needle, haystack))
