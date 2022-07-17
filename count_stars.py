
import skimage.io
import numpy as np


def brightness(pixel):
	"""Sums RGB values in pixel to yield brightness."""
	return int(pixel[0]) + int(pixel[1]) + int(pixel[2])


def calculate_threshold(image):
	"""Gets the average brightness of all pixels as a 'brightness threshold' which will be used for identifying stars."""
	height, width, pix_depth = np.shape(image)
	pixels = np.reshape(image, (height*width, pix_depth))
	brightnesses = [brightness(pixel) for pixel in pixels]
	return sum(brightnesses) / len(brightnesses)


def main(filename="stars_image.jpg"):
	image = skimage.io.imread(fname=filename)
	brightness_threshold = calculate_threshold(image)
	visited_pixels = set()

	return 0
