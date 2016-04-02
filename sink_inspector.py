from scipy.misc import imread
from skimage.feature import canny, peak_local_max
from skimage import morphology
from skimage.io import imread
from skimage import filters
from itertools import chain
from collections import namedtuple
from utils import draw_res
from skimage import exposure 
from skimage.draw import circle_perimeter
from skimage import color
from scipy import ndimage as ndi

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

    return dt < 20 and rd < 15


def count_dishes(out, sink):
    edges = canny(
        sink,
        sigma=2,
        #low_threshold=10,
        high_threshold=0.3
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

    for idx in np.argsort(accums)[::-1][:25]:
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


    dishes = [k for k,v in hits.iteritems()]

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

def adjust_brightness_gamma_log(sink):
    sink = exposure.adjust_gamma(sink, 3, 1)
    sink = exposure.adjust_log(sink, 2)
    return sink

def get_dirtiness(f, out=None):
    sink = get_sink(f)
    sink = sink[60:450, 180:440]
    #sink = adjust_brightness(sink)
    sink = adjust_brightness_gamma_log(sink)

    dishes = count_dishes(out, sink)
    edges = count_edges(sink)
    score = edges * (dishes + 1)

    return Dirtiness(score, edges, dishes)

def adjust_brightness(sink):
    sink = sink.copy()

    pmin, pmax = np.percentile(sink, (2, 98))

    nsink = exposure.rescale_intensity(
        sink,
        in_range=(pmin, pmax)
    )

    sink = exposure.equalize_hist(sink)

    # Adaptive Equalization
    return exposure.equalize_adapthist(
        sink,
        clip_limit=0.02
    )

def get_sink(f):
    return imread(f, True)



if __name__ == '__main__':
    sinks = [
        #'tests/sample_files/1d/16_03_31_18:53.jpg',
        #'tests/sample_files/4d_2g/16_03_31_15:33.jpg',
        #'tests/sample_files/4d_2g/16_03_31_16:33.jpg',
        'tests/sample_files/4d_2g/16_03_31_16:43.jpg',
        #'tests/sample_files/1d_1g/16_04_01_12:14.jpg',
        #'tests/sample_files/1d_1g/16_04_01_04:04.jpg'
        #'tests/sample_files/1d_1g/16_04_01_03:04.jpg',
        #'tests/sample_files/2d_1g/16_04_01_21:25.jpg',
        #'tests/sample_files/1d_1g/16_04_01_06:44.jpg',
        #'tests/sample_files/1d_1g/16_04_01_03:24.jpg',
        #'tests/sample_files/1d_1g/16_04_01_03:14.jpg',
    ]

    for sink in sinks:
        d = get_dirtiness(sink, sys.argv[1])
        print('{}: {}'.format(sink, d))
