import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('data/0954P.jpg')
# img = cv.imread('data/wall_0940P_bed_frame_0267P.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)

plt.figure()
f, axarr = plt.subplots(3, 1)
axarr[0].imshow(thresh, cmap='gray')
plt.title("initial threshold")

# noise removal
kernel = np.ones((3, 3), np.uint8)
opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=3)
axarr[1].imshow(opening, cmap='gray')
plt.title("After opening")

# sure background area
sure_bg = cv.dilate(opening, kernel, iterations=5)
axarr[2].imshow(opening, cmap='gray')
plt.title("After dilation")
plt.show()

# Finding sure foreground area
# dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
# ret, sure_fg = cv.threshold(dist_transform, 0.3*dist_transform.max(), 255, 0)
# plt.imshow(sure_fg)
# plt.show()
#
# # Finding unknown region
# sure_fg = np.uint8(sure_fg)
# unknown = cv.subtract(sure_bg, sure_fg)
# sure_bg = np.uint8(sure_bg)
unknown = cv.subtract(gray, sure_bg)

# Marker labelling
ret, markers = cv.connectedComponents(unknown)
# Add one to all labels so that sure background is not 0, but 1
markers = markers+1
# Now, mark the region of unknown with zero
markers[unknown == 255] = 0  # TODO

markers = cv.watershed(img, markers)
plt.figure()
f, axarr = plt.subplots(2, 1)
axarr[0].imshow(markers)

img[markers == -1] = [255, 0, 0]
axarr[1].imshow(img)
plt.show()
