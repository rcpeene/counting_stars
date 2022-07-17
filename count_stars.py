
import skimage.io
import numpy as np


brightness_threshold = 0
n_stars = 0


def brightness(pixel):
	"""Sums RGB values in pixel to yield brightness."""
	return int(pixel[0]) + int(pixel[1]) + int(pixel[2])


def calculate_threshold(image):
	"""Gets the average brightness of all pixels as a 'brightness threshold' which will be used for identifying stars."""
	height, width, px_depth = np.shape(image)
	pixels = np.reshape(image, (height*width, px_depth))
	# print("calculating threshold")
	brightnesses = [brightness(pixel) for pixel in pixels]
	# print("threshold calcualted")
	return (sum(brightnesses) / len(brightnesses)) * 6


def adjacent_pixels(image, px_loc):
	"""Returns a list of the locations of the orthogonally adjacent pixels to a given pixel location, where each pixel location is represented as a tuple of the form (row, col)"""
	height, width, px_depth = np.shape(image)
	row, col = px_loc

	adj_px_locs = []
	if row != height-1:
		adj_px_locs.append((row+1, col))
	if row != 0:
		adj_px_locs.append((row-1, col))
	if col != width-1:
		adj_px_locs.append((row, col+1))
	if col != 0:
		adj_px_locs.append((row, col-1))
	return adj_px_locs


def mark_cluster(image, px_loc, visited_pixels, size):
	# print("mark_cluster")
	global brightness_threshold

	visited_pixels.add(px_loc)
	for adj_px_loc in adjacent_pixels(image, px_loc):
		if adj_px_loc in visited_pixels:
			continue
		if brightness(image[adj_px_loc]) > brightness_threshold:
			size += mark_cluster(image, adj_px_loc, visited_pixels, size+1)
	return size


def main(filename="samples/sample1.jpg"):
	global brightness_threshold
	global n_stars

	image = skimage.io.imread(fname=filename)
	brightness_threshold = calculate_threshold(image)
	# print("threshold:",brightness_threshold)
	visited_pixels = set()

	height, width, px_depth = np.shape(image)
	for row in range(height):
		for col in range(width):
			if (row,col) in visited_pixels:
				continue
			if brightness(image[row,col]) > brightness_threshold:
				# print(f"counting star at {row}, {col} with brightness:",brightness(image[row,col]))
				n_stars += 1
				size = mark_cluster(image, (row,col), visited_pixels, 1)
				# print(f"cluster at {row}, {col} of size {size}\n")

	# print("threshold was:",brightness_threshold)
	# print("count:",n_stars)
	return n_stars


if __name__ == "__main__":
	main()
