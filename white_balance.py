import numpy as np


def grayworld_wb(image: np.ndarray):
    """
    White balances the image assuming that the average color should be gray with shape [N, M, 3]
    :param image: a numpy array with values between 0 and 1 representing the image
    :return: the white balanced image
    """
    ratio = np.mean(image)/np.mean(image, axis=(0, 1))
    return np.clip(image*ratio[None, None, :], 0, 1)


def quantile_wb(image: np.ndarray, quantile: float=.97):
    """
    White balances an image with the assumption that the white value is an upper value of the quantiles
    :param image: a numpy array with values between 0 and 1 representing the image with shape [N, M, 3]
    :param quantile: which quantile to use (between 0 and 1) - the default is 97%
    :return: the white balanced image
    """
    return (image * 1.0 / np.percentile(image, quantile*100, axis=(0, 1))).clip(0, 1)


def groundtruth_wb(image: np.ndarray, white_patch: np.ndarray):
    """
    White balances an image using a ground truth white patch
    :param image: a numpy array with values between 0 and 1 representing the image with shape [N, M, 3]
    :param white_patch: a white patch from the image with shape [q, q, 3]
    :return: the white balanced image
    """
    ratio = np.mean(white_patch)/np.mean(white_patch, axis=(0, 1))
    return np.clip(image*ratio[None, None, :], 0, 1)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    image = plt.imread('data\\0408P.jpg')/255

    plt.figure()
    plt.imshow(image)
    plt.title('original')
    plt.axis('off')

    plt.figure()
    plt.imshow(grayworld_wb(image))
    plt.title('grayworld')
    plt.axis('off')

    plt.figure()
    plt.imshow(quantile_wb(image, .97))
    plt.title('quantile .97')
    plt.axis('off')

    plt.figure()
    plt.imshow(quantile_wb(image, .999))
    plt.title('quantile .999')
    plt.axis('off')

    plt.figure()
    plt.imshow(groundtruth_wb(image, image[:10, :10]))
    plt.title('groundtruth')
    plt.axis('off')

    plt.show()
