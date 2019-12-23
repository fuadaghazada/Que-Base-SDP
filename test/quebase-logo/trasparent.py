from copy import deepcopy

import cv2
import numpy as np

PATH = 'logo.png'

# Reading the image as grayscale
image = cv2.imread(PATH)

# Coolor conversion
updatedImage = deepcopy(image)
updatedImage = cv2.cvtColor(updatedImage, cv2.COLOR_BGR2BGRA)

# Cropping
height, width, _ = updatedImage.shape
updatedImage = updatedImage[0:height, 0:width // 2 - 14]
height, width, _ = updatedImage.shape

# Zero out the alpha channel for the pixels that is not 0 (black)
for i in range(width):
    for j in range(height):
        pixel = updatedImage[j, i]

        if pixel[0] != 0 and pixel[1] != 0 and pixel[2] != 0:
            updatedImage[j, i][0] = 255
            updatedImage[j, i][1] = 255
            updatedImage[j, i][2] = 255
            updatedImage[j, i][3] = 0

# Eroding/Dilating for removing the noise
filter = np.ones((2, 2), np.uint8)
updatedImage = cv2.erode(updatedImage, filter, iterations=1)
filter = np.ones((3, 3), np.uint8)
updatedImage = cv2.dilate(updatedImage, filter, iterations=1)


# Saving
cv2.imwrite('trasparent.png', updatedImage)
