
import sys
import count_stars


def main():
	try:
		sample_num = sys.argv[1]
	except:
		print("No sample number given as first command line argument")
		return
	try:
		sample_num = int(sample_num)
	except:
		print("Sample number must be an integer")
		return

	fd = open(f"samples/Annotation.txt")
	labels = fd.readlines()
	try:
		label = labels[sample_num-1]
		value = label.split(":")[1]
		value = int(value[1:-1])
	except:
		print("There is no valid label for that sample number")
		return

	count = count_stars.main(f"samples/sample{sample_num}.jpg")
	print("labeled value:",value)
	print("counted value:",count)

main()
