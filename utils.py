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


from itertools import permutations

n = 8
cols = range(n)
for vec in permutations(cols):
    if n == len(set(vec[i]+i for i in cols)) \
         == len(set(vec[i]-i for i in cols)):
        print ( vec )


# Examples to render Irene
class Counter(object):

    def __init__(self, start=0):
        self.v = start

    def increase(self):
        self.v += 1

    def decrease(self):
        self.v -= 1


@presentation.render_for(Counter)
def render(self, h, comp, *args):
    with h.div(class_='counter'):
        h << h.div(self.v)

        with h.span:
            h << h.a('--').action(self.decrease)

        with h.span:
            h << h.a('++').action(self.increase)

    return h.root
