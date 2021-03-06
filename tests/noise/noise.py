import numpy as np
import os
import cv2


def noisy(noise_typ, image):
    if noise_typ == "gauss":
        row, col, ch = image.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = image + gauss
        return noisy
    elif noise_typ == "s&p":
        # salt-and-pepper noise
        row, col, ch = image.shape
        s_vs_p = 0.5
        # This is the amount of noise
        amount = 0.002
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        out[coords] = 1
        # Pepper mode
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        out[coords] = 0
        return out
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy
    elif noise_typ == "speckle":
        row, col, ch = image.shape
        gauss = np.random.randn(row, col, ch)
        gauss = gauss.reshape(row, col, ch)
        noisy = image + image * gauss
        return noisy

img = cv2.imread('silent-night.jpg')
cv2.imshow('IMG', img)
noisy_img = noisy('s&p', img)
noisy_img = cv2.cvtColor(noisy_img, cv2.COLOR_BGR2GRAY)
cv2.imshow('NOISY', noisy_img)
# blur = cv2.GaussianBlur(noisy_img, (5, 5), 0)
blur = cv2.medianBlur(img, 1)
cv2.imshow('BLUR', blur)
cv2.waitKey(0)
