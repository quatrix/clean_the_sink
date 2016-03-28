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

def count_circules(sink):
    sink = sink[195:330, 253:350]

    edges = canny(
        sink,
        sigma=1,
        low_threshold=0.1,
        high_threshold=0.7
    )

    # Detect two radii
    hough_radii = np.arange(10, 100, 1)
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

    for idx in np.argsort(accums)[::-1][:5]:
        center_x, center_y = centers[idx]
        radius = radii[idx]
        
        # removing circules that are 
        # too close to each other
        found = False
        for d in drawn:
            dx, dy = d

            distance = math.hypot(
                center_x - dx,
                center_y - dy
            )

            if distance < 20:
                found = True
                break

        if found:
            continue

        drawn.append((center_x, center_y))

        cx, cy = circle_perimeter(center_y, center_x, radius)
        try:
            sink[cy, cx] = (220, 20, 20)
        except IndexError:
            continue

    #draw_res(sink, edges)
    #print(len(drawn))
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


def get_dirtiness(f):
    sink = imread(f, True)
    sink = adjust_gamma(sink, 1, 2)
    circules = count_circules(sink) + 1
    edges = count_edges(sink)
    return edges * circules


if __name__ == '__main__':
    sinks = [
        "one_glass_dl",
        "2d_dl",
        "3d_dl",
        "4d_dl",
        "lots_dl",
        "one_glass_ll",
        "half_dirty_partially_dark",
        "half_dirty",
        "washing_dishes",
        "watering_plants",
        "clean_dl",
        "clean_ll",
        "clean2_ll",
    ]

    for sink in sinks:
        f = 'tests/sample_files/' + sink + '.jpg'
        d = get_dirtiness(f)
        print('{}: {}'.format(sink, d))
