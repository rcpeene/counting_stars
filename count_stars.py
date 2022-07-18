
import skimage.io
import numpy as np


brightness_threshold = 0


def brightness(pixel):
	"""Sums RGB values in pixel to yield brightness."""
	return int(pixel[0]) + int(pixel[1]) + int(pixel[2])


def calculate_threshold(image):
	"""Determines a 'brightness threshold' which will be used for identifying stars based on the average and maximum pixel brightnesses in the image"""
	height, width, px_depth = np.shape(image)
	pixels = np.reshape(image, (height*width, px_depth))
	brightnesses = [brightness(pixel) for pixel in pixels]
	max_brightness = max(brightnesses)
	avg_brightness = sum(brightnesses) / len(brightnesses)
	# threshold is top 80% brightness between average and maximum
	return avg_brightness + ( (max_brightness-avg_brightness) / 5 )


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
	"""Recursively radiates outward from px_loc, marking every unvisited pixel which is bright enough to be considered part of a star as 'visited', stopping when there are no more unvisited bright pixels in a contiguous space."""
	# print("mark_cluster")
	global brightness_threshold

	visited_pixels.add(px_loc)
	for adj_px_loc in adjacent_pixels(image, px_loc):
		if adj_px_loc in visited_pixels:
			continue
		if brightness(image[adj_px_loc]) > brightness_threshold:
			size += mark_cluster(image, adj_px_loc, visited_pixels, size+1)
	return size


def main(filename="stars_image.jpg"):
	"""Counts the number of stars in a given image. First, this calculates a 'brightness threshold' which is used to determine if a given pixel is bright enough to be part of a star. Then, initializes an empty list of 'visited pixels. Finally, scans through all unvisited pixels in the image. If a pixel is bright enough to be a star, increment n_stars, and mark all pixels in that cluster as a visited.'"""
	global brightness_threshold
	n_stars = 0

	image = skimage.io.imread(fname=filename)
	brightness_threshold = calculate_threshold(image)
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

	print("threshold was:",brightness_threshold)
	print("count:",n_stars)
	return n_stars


if __name__ == "__main__":
	main()
