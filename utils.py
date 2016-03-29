import matplotlib.pyplot as plt

def draw_res(out, *fs):
    if out is None:
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
    plt.savefig(out)
