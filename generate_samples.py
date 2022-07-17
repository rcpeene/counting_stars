
import skimage.io
import numpy as np


def main():
	"""Takes the image of interest and divides it into 100 sub-images to serve as samples which will be manually annotated and used for testing and evaluation."""

	image = skimage.io.imread(fname="stars_image.jpg")
	height, width, pix_depth = np.shape(image)
	sample_height = height // 10
	sample_width = width // 10

	sample_num = 0
	for i in range(10):
		top_bnd = i * sample_height
		bot_bnd = (i+1) * sample_height

		for j in range(10):
			sample_num += 1
			lft_bnd = j * sample_width
			rgt_bnd = (j+1) * sample_width

			sample = image[top_bnd:bot_bnd, lft_bnd:rgt_bnd]
			skimage.io.imsave(f"samples/sample{sample_num}.jpg", sample)


main()
