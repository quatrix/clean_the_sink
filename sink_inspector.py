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
import sys

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

sink_x, sink_y, sink_r = (191, 189, 25)

def is_sink_hole(x, y, r):
    dt = distance(x, sink_x, y, sink_y)
    rd = abs(r - sink_r)

    return dt < 10 and rd < 10


def count_dishes(out, sink):
    edges = canny(
        sink,
        sigma=2,
        low_threshold=0.1,
        high_threshold=0.2,
    )
    
    hough_radii = np.arange(25, 70, 1)
    hough_res = hough_circle(edges, hough_radii)
    centers = []
    accums = []
    radii = []

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

        if is_sink_hole(center_x, center_y, radius):
            continue

        for d in hits.keys():
            dx, dy, dr = d

            dt = distance(center_x, dx, center_y, dy)
            
            if dt <= 40 and abs(dr - radius) < 50:
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

    draw_res(out, sink, edges)
    return len(dishes)


def count_edges(sink):
    edges = canny(sink, sigma=1)
    return sum([int(i) for i in chain(*edges)])


def get_dirtiness(f, out=None):
    sink = get_sink(f)
    sink = sink[60:450, 180:440]
    sink = adjust_brightness(sink)

    dishes = count_dishes(out, sink)
    #edges = count_edges(sink)
    edges = 1
    score = edges * (dishes + 1)

    return Dirtiness(score, edges, dishes)

def get_brightness(i):
    all_pixels = list(chain(*i))
    return sum(all_pixels) / len(all_pixels)

def adjust_brightness(sink):
    nsink = sink.copy()
    brightness = get_brightness(sink)

    print(brightness)
    if brightness < 0.42:
        p0 = 3
    elif brightness < 0.46:
        p0 = 4
    elif brightness < 0.47:
        p0 = 6
    elif brightness < 0.5:
        p0 = 5
    elif brightness < 0.52:
        p0 = 6
    else:
        p0 = 5

    pmin, pmax = np.percentile(nsink, (p0, 98))

    nsink = exposure.rescale_intensity(
        nsink,
        in_range=(pmin, pmax)
    )

    nsink = exposure.equalize_hist(nsink)

    # Adaptive Equalization
    return exposure.equalize_adapthist(
        nsink,
        clip_limit=0.02
    )

def get_sink(f):
    return imread(f, True)



if __name__ == '__main__':
    sinks = [
        #'tests/sample_files/4d_2g/16_03_31_07:22.jpg',
        #'tests/sample_files/4d_2g/16_03_30_12:21.jpg',
        #'tests/sample_files/4d_2g/16_03_31_07:42.jpg',
        #'tests/sample_files/4d_2g/16_03_31_05:02.jpg',
        'tests/sample_files/1d.jpg',
    ]

    for sink in sinks:
        d = get_dirtiness(sink, sys.argv[1])
        print('{}: {}'.format(sink, d))
