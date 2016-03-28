import matplotlib.pyplot as plt
import sys

def draw_res(*fs):
    if len(sys.argv) == 1:
        return

    fig, axs = plt.subplots(nrows=1,
        ncols=len(fs),
        figsize=(8, 3),
        sharex=True,
        sharey=True
    )

    for (ax, f) in zip(axs, fs):
        ax.axis('on')
        ax.imshow(f, cmap=plt.cm.gray)

    fig.tight_layout()
    plt.savefig(sys.argv[1])
