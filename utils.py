from collections import deque
from itertools import islice


def window(iterable, size=2):
    iterable = iter(iterable)
    d = deque(islice(iterable, size), size)
    yield d
    for x in iterable:
        d.append(x)
        yield d

for win in window('abcdefghijkl', 3):
    print('-'.join(win))
