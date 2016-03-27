from scipy.misc import imread
from skimage.feature import canny
from skimage.io import imread
from skimage import color
from itertools import chain

from skimage.exposure import adjust_gamma


def get_sink(f):
    sink = imread(f, True)
    buttom_sink = sink[195:330, 253:350]
    top_sink = sink[160:195, 253:315]

    return top_sink, buttom_sink


def get_edges(sink):
    sink = adjust_gamma(sink, 1, 2)
    edges = canny(sink, sigma=0.01)
    return sum([int(i) for i in chain(*edges)])


def get_dirtiness(f):
    sink_parts = get_sink(f)
    return sum(get_edges(part) for part in sink_parts)

if __name__ == '__main__':

    for f in files:
        print("{} -> {}".format(f, get_dirtiness(f)))
