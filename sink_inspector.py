from scipy.misc import imread
from skimage.feature import canny, peak_local_max
from skimage.io import imread
from skimage import color
from itertools import chain
from utils import draw_res
from skimage.exposure import adjust_gamma
from skimage.draw import circle_perimeter
from skimage import color
import math

from skimage.transform import hough_circle
import numpy as np

def distance(x1, x2, y1, y2):
    return math.hypot(
        x1 - x2,
        y1 - y2,
    )

def is_fosset(x, y, radius):
    a = 30 > x > 0
    b = 80 > y > 60
    c = 13 >= radius >= 6

    return a and b and c


def is_sink_hole(x, y, radius):
    dx, dy = 87, 74

    rd = 15 > radius > 5
    dist = distance(x, dx, y, dy)
    
    return dist <= 12 and rd

def count_dishes(sink):
    sink = sink[160:330, 250:350]

    edges = canny(
        sink,
        sigma=0,
        low_threshold=0.1,
        high_threshold=0.2
    )

    # Detect two radii
    hough_radii = np.arange(9, 60, 1)
    hough_res = hough_circle(edges, hough_radii)
    centers = []
    accums = []
    radii = []
    drawn = []

    for radius, h in zip(hough_radii, hough_res):
        # For each radius, extract two circles
        num_peaks = 2
        peaks = peak_local_max(h, num_peaks=num_peaks)
        centers.extend(peaks)
        accums.extend(h[peaks[:, 0], peaks[:, 1]])
        radii.extend([radius] * num_peaks)

    sink = color.gray2rgb(sink)

    for idx in np.argsort(accums)[::-1][:10]:
        center_x, center_y = centers[idx]
        radius = radii[idx]

        
        # removing circules that are 
        # too close to each other
        found = False
        for d in drawn:
            dx, dy, dr = d

            if distance(center_x, dx, center_y, dy) < 20: 
                found = True
                break

        if found:
            continue

        if is_sink_hole(center_x, center_y, radius):
            continue

        if is_fosset(center_x, center_y, radius):
            continue

        drawn.append((center_x, center_y, radius))

        cx, cy = circle_perimeter(center_y, center_x, radius)
        try:
            sink[cy, cx] = (220, 20, 20)
        except IndexError:
            continue

    draw_res(sink, edges)
    print(drawn)
    return len(drawn)

def count_edges(sink):
    # cropping out parts of the sink
    # we don't want to take into account
    parts = sink[195:330, 253:350], \
           sink[160:195, 253:315]

    return sum(
        _count_edges(part)
        for part in parts
    )


def _count_edges(sink):
    edges = canny(sink, sigma=0.01)
    return sum([int(i) for i in chain(*edges)])


def get_sink(f):
    return adjust_gamma(imread(f, True), 1, 1.5)

def get_dirtiness(f):
    sink = get_sink(f)
    dishes = count_dishes(sink) + 1
    edges = count_edges(sink)
    return edges * dishes


if __name__ == '__main__':
    sinks = [
        #"one_glass_dl",
        #"2d_dl",
        #"3d_dl",
        #"4d_dl",
        #"lots_dl",
        #"one_glass_ll",
        #"half_dirty_partially_dark",
        #"half_dirty",
        #"washing_dishes",
        #"watering_plants",
        "clean_dl",
        "clean2_dl",
        "clean_ll",
        "clean2_ll",
        #"2d_2g_dl_0",
        #"2d_2g_dl_1",
    ]

    for sink in sinks:
        f = 'tests/sample_files/' + sink + '.jpg'
        d = get_dirtiness(f)
        print('{}: {}'.format(sink, d))
