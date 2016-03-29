from scipy.misc import imread
from skimage.feature import canny, peak_local_max
from skimage.io import imread
from skimage import filters
from itertools import chain
from collections import namedtuple
from utils import draw_res
from skimage import exposure 
from skimage.draw import circle_perimeter
from skimage import color
import math

from skimage.transform import hough_circle
import numpy as np

Dirtiness = namedtuple(
    'Dirtiness', ['score', 'edges', 'dishes']
)


def distance(x1, x2, y1, y2):
    return math.hypot(
        x1 - x2,
        y1 - y2,
    )


def count_dishes(sink):
    edges = canny(
        sink,
        sigma=2,
        low_threshold=0.1,
        high_threshold=0.5,
    )
    
    hough_radii = np.arange(25, 70, 1)
    hough_res = hough_circle(edges, hough_radii)
    centers = []
    accums = []
    radii = []
    drawn = []

    for radius, h in zip(hough_radii, hough_res):
        num_peaks = 2
        peaks = peak_local_max(h, num_peaks=num_peaks)
        centers.extend(peaks)
        accums.extend(h[peaks[:, 0], peaks[:, 1]])
        radii.extend([radius] * num_peaks)

    sink = color.gray2rgb(sink)
    hits = {}

    for idx in np.argsort(accums)[::-1]:
        center_x, center_y = centers[idx]
        radius = radii[idx]

        for d in hits.keys():
            dx, dy, dr = d

            dt = distance(center_x, dx, center_y, dy)
            
            if dt <= 30 and abs(dr - radius) < 40:
                hits[d] += 1
                break
        else:
            hits[(center_x, center_y, radius)] = 1


    dishes = [k for k,v in hits.iteritems() if v > 5]

    for dish in dishes:
        center_x, center_y, radius = dish

        cx, cy = circle_perimeter(center_y, center_x, radius)

        try:
            sink[cy, cx] = (220, 250, 20)
        except IndexError:
            continue

    draw_res(sink, edges)
    return len(dishes)


def count_edges(sink):
    edges = canny(sink, sigma=1)
    return sum([int(i) for i in chain(*edges)])


def get_dirtiness(f):
    sink = get_sink(f)
    sink = sink[60:450, 180:440]
    sink = adjust_brightness(sink)

    dishes = count_dishes(sink)
    edges = count_edges(sink)
    score = edges * (dishes + 1)

    return Dirtiness(score, edges, dishes)


def adjust_brightness(sink):
    nsink = sink.copy()
    pmin, pmax = np.percentile(nsink, (3, 98))

    nsink = exposure.rescale_intensity(
        nsink,
        in_range=(pmin, pmax)
    )

    nsink = exposure.equalize_hist(nsink)

    # Adaptive Equalization
    return exposure.equalize_adapthist(
        nsink,
        clip_limit=0.01
    )

def get_sink(f):
    return imread(f, True)



if __name__ == '__main__':
    sinks = [
        "4d_2g_dl_0",
        "4d_2g_ll_0",
    ]

    for sink in sinks:
        f = 'tests/sample_files/' + sink + '.jpg'
        d = get_dirtiness(f)
        print('{}: {}'.format(sink, d))
