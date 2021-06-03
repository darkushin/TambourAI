import numpy as np
import pickle
from scipy.special import logsumexp

with open('color_dict.pkl', 'rb') as f:
    color_dict = pickle.load(f)

rgbs = np.array([k for k in color_dict.keys()])/255
rgbs_raw = [k for k in color_dict.keys()]
codes = [color_dict[k][-1] for k in color_dict.keys()]


def mean_color(patches: np.ndarray, top: int=5):
    """
    Find top-k mean colors from patches
    :param patches: a numpy array with shape [N, patch_w, patch_h, 3] where N is the number of
                    patches, in the range [0,1]
    :param top: an int of how many colors to return
    :return: a tuple of rgbs and codes
    """
    dists = rgbs[None, :, None, None, :] - patches[:, None]
    dists = np.mean(dists**2, axis=(0, 2, 3, 4))
    inds = np.argsort(dists)[:top]
    return [rgbs_raw[i] for i in inds], [codes[i] for i in inds]


def center_color(patches: np.ndarray, top: int=5, sigma: float=1):
    """
    Find top-k mean colors from patches, giving higher weight to the center pixel of each patch
    :param patches: a numpy array with shape [N, patch_w, patch_h, 3] where N is the number of
                    patches, in the range [0, 1]
    :param top: an int of how many colors to return
    :param sigma: size of mask around center pixel
    :return: a tuple of rgbs and codes
    """
    xx, yy = np.meshgrid(np.arange(patches.shape[1]), np.arange(patches.shape[2]))
    xx, yy = xx - patches.shape[1]//2, yy - patches.shape[2]//2
    mask = (xx**2 + yy**2 - 2*xx*yy)/(2*sigma)
    mask = np.exp(mask - logsumexp(mask))
    dists = rgbs[None, :, None, None, :] - patches[:, None]
    dists = np.mean(mask[None, None, :, :, None]*dists**2, axis=(0, 2, 3, 4))
    inds = np.argsort(dists)[:top]
    return [rgbs_raw[i] for i in inds], [codes[i] for i in inds]


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    image = plt.imread('data\\0408P.jpg') / 255

    patches = np.array([image[i:i+8, j:j+8] for i in range(3) for j in range(3)])
    print(mean_color(patches))
    print(center_color(patches, sigma=.0001))
