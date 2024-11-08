import random
import numpy as np


def random_flip_all_axes(x, y, prob=0.5):
    """
    Randomly flip paired 3D images (e.g., scans and labels) along one or multiple axes

    Input:
    - x: 3D image, optionally with an additional axis for multiple modalities. Shape: (optional channel dimension), width, height, depth
    - y: image to transform in the same way as x. Shape: same as x.
    - prob: flip probability for each of the three iterations
    """
    # augmentation by flipping
    cnt = 3
    while random.random() < prob and cnt > 0:
        degree = random.choice([-1, -2, -3])
        x = np.flip(x, axis=degree)
        y = np.flip(y, axis=degree)
        cnt = cnt - 1

    return x, y
