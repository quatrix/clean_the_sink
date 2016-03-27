from PIL import Image, ImageDraw
import numpy as np

from skimage.draw import circle_perimeter
from skimage.feature import peak_local_max, canny
from skimage.transform import hough_circle
from skimage.util import img_as_ubyte
from scipy.misc import fromimage
from skimage.io import imread
from skimage import color
from skimage import feature

from itertools import chain
import matplotlib.pyplot as plt



def get_sink(f):
    # left, top, right, bottom
    return Image.open(f).crop((250, 155, 350, 330))



def make_bigger(i):
    basewidth = 300
    wpercent = (basewidth/float(i.size[0]))
    hsize = int((float(i.size[1])*float(wpercent)))
    return i.resize((basewidth,hsize), Image.ANTIALIAS)

def remove_fosset(i):
    draw = ImageDraw.Draw(i)
    draw.rectangle([(300, 0), (150, 100)], fill=(127,127,127))
    return i



def get_edges(im):
    edges1 = feature.canny(im, sigma=1)
    #return sum([int(i) for i in chain(*edges1)])
    # display results
    edges2 = feature.canny(im, sigma=3)
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3),
                                        sharex=True, sharey=True)

    ax1.imshow(im, cmap=plt.cm.gray)
    ax1.axis('off')
    ax1.set_title('noisy image', fontsize=20)

    ax2.imshow(edges1, cmap=plt.cm.gray)
    ax2.axis('off')
    ax2.set_title('Canny filter, $\sigma=1$', fontsize=20)

    ax3.imshow(edges2, cmap=plt.cm.gray)
    ax3.axis('off')
    ax3.set_title('Canny filter, $\sigma=3$', fontsize=20)

    fig.tight_layout()
    plt.savefig('myfig')

def convert_to_skimage_format(i):
    i.save('/tmp/out.jpg')
    return imread('/tmp/out.jpg', True)


def get_dirtiness(f):
    sink = get_sink(f)
#    sink = make_bigger(sink)
#    sink = remove_fosset(sink)
    sink = convert_to_skimage_format(sink)
    return get_edges(sink)


def main():
    files = [
#        "half_dirty.jpg",
#        "half_dirty_partially_dark.jpg",
#        "washing_dishes.jpg",
#        "watering_plants.jpg",
#        "2d_dl.jpg",
#        "3d_dl.jpg",
        "4d_dl.jpg",
#        "clean_dl.jpg",
    ]

    for f in files:
        print("{} -> {}".format(f, get_dirtiness(f)))

if __name__ == '__main__':
    main()
