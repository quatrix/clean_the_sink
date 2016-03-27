from PIL import Image, ImageDraw, ImageEnhance
import numpy as np

from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average

from skimage.filters import threshold_otsu, threshold_adaptive
from skimage.filters import sobel, roberts, scharr
from scipy import ndimage as ndi
from skimage.draw import circle_perimeter
from skimage.feature import peak_local_max, canny
from skimage.transform import hough_circle
from skimage.util import img_as_ubyte, crop
from scipy.misc import fromimage
from skimage.io import imread
from skimage import color
from skimage import feature
from skimage.morphology import watershed
from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
from matplotlib.path import Path



from itertools import chain
import matplotlib.pyplot as plt



def get_sink(f):
    sink = imread(f, True)
    #whole_sink = sink[160:330, 253:350]
    buttom_sink = sink[195:330, 253:350]
    top_sink = sink[160:195, 253:315]

    return top_sink, buttom_sink





def make_bigger(i):
    basewidth = 300
    wpercent = (basewidth/float(i.size[0]))
    hsize = int((float(i.size[1])*float(wpercent)))
    return i.resize((basewidth,hsize), Image.ANTIALIAS)

def remove_fosset(i):
    draw = ImageDraw.Draw(i)
    draw.rectangle([(60, 0), (100, 40)], fill=(227,227,227))
    return i

def get_edges(sink):
    edges = feature.canny(sink, sigma=0.1)
    return sum([int(i) for i in chain(*edges)])


    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3), sharex=True, sharey=True)

    ax1.imshow(sink, cmap=plt.cm.gray)
    ax1.axis('off')
    ax1.set_title('sink', fontsize=20)


    ax2.imshow(edges, cmap=plt.cm.gray)
    ax2.axis('off')
    ax2.set_title('result', fontsize=20)

    """
    block_size = 101
    result = threshold_adaptive(coins, block_size, offset=100)

    global_thresh = threshold_otsu(coins)
    result = coins > global_thresh


    edges1 = feature.canny(im, sigma=1)
    filled_dishes = ndi.binary_fill_holes(edges1)
    label_objects, nb_labels = ndi.label(filled_dishes)
    sizes = np.bincount(label_objects.ravel())
    mask_sizes = sizes > 20
    mask_sizes[0] = 0
    coins_cleaned = mask_sizes[label_objects]
    #return sum([int(i) for i in chain(*edges1)])
    # display results
    edges2 = feature.canny(im, sigma=3)



    ax3.imshow(edges2, cmap=plt.cm.gray)
    ax3.axis('off')
    ax3.set_title('Canny filter, $\sigma=3$', fontsize=20)

    fig.tight_layout()
    """
    plt.savefig('myfig')

def get_dirtiness(f):
    sink_parts = get_sink(f)
    #sink = make_bigger(sink)
    #sink = remove_fosset(sink)
    return sum(get_edges(part) for part in sink_parts)



def main():

    files = [
        "half_dirty.jpg",
        "half_dirty_partially_dark.jpg",
        "washing_dishes.jpg",
        "watering_plants.jpg",
        "2d_dl.jpg",
        "3d_dl.jpg",
        "4d_dl.jpg",
        "lots_dl.jpg",
        "one_glass_dl.jpg",
        "clean_dl.jpg",
    ]

    for f in files:
        print("{} -> {}".format(f, get_dirtiness(f)))

if __name__ == '__main__':
    main()
