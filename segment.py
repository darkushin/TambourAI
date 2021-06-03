import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from white_balance import grayworld_wb

# img = cv.imread('data/0874D.jpg')
# img = cv.imread('data/wall_0940P_bed_frame_0267P.jpg')


def segment(img):
    img = (img*255).astype(np.uint8)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)

    # f, axarr = plt.subplots(3, 1)
    # axarr[0].imshow(thresh, cmap='gray')
    # plt.title("initial threshold")

    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=3)
    # axarr[1].imshow(opening, cmap='gray')
    # plt.title("After opening")

    # sure background area
    sure_bg = cv.dilate(opening, kernel, iterations=5)
    # axarr[2].imshow(opening, cmap='gray')
    # plt.title("After dilation")
    # plt.show()

    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    ret, sure_fg = cv.threshold(dist_transform, 0.5*dist_transform.max(), 255, 0)
    # plt.imshow(sure_fg)
    # plt.title("sure foreground")
    # plt.show()

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg, sure_fg)

    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0

    markers = cv.watershed(img, markers)
    # f, axarr = plt.subplots(2, 1)
    # axarr[0].imshow(markers)

    img[markers == -1] = [255, 0, 0]
    # img[markers == markers.max()] = [0, 255, 0]
    # mask = np.zeros_like(img)
    # mask[markers == markers.max()] = [0, 255, 0]
    # axarr[1].imshow(mask)
    return img, markers


def get_patches(img, markers):
    bg = img[markers == markers.max()]


if __name__ == "__main__":
    # img = cv.imread('data/wall_0940P_bed_frame_0267P.jpg')
    image = plt.imread('data\\0129T.jpg') / 255
    segment(grayworld_wb(image))
