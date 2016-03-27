from scipy.misc import imread
from skimage.feature import canny
from skimage.io import imread
from skimage import color
from itertools import chain


def get_sink(f):
    sink = imread(f, True)
    buttom_sink = sink[195:330, 253:350]
    top_sink = sink[160:195, 253:315]

    return top_sink, buttom_sink


def get_edges(sink):
    edges = canny(sink, sigma=0.1)
    return sum([int(i) for i in chain(*edges)])


def get_dirtiness(f):
    sink_parts = get_sink(f)
    return sum(get_edges(part) for part in sink_parts)

if __name__ == '__main__':
    files = [
        "sample_files/half_dirty.jpg",
        "sample_files/half_dirty_partially_dark.jpg",
        "sample_files/washing_dishes.jpg",
        "sample_files/watering_plants.jpg",
        "sample_files/2d_dl.jpg",
        "sample_files/3d_dl.jpg",
        "sample_files/4d_dl.jpg",
        "sample_files/lots_dl.jpg",
        "sample_files/one_glass_dl.jpg",
        "sample_files/clean_dl.jpg",
    ]

    for f in files:
        print("{} -> {}".format(f, get_dirtiness(f)))
