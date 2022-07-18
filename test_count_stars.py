
import sys
import count_stars


def test_sample(sample_num, labels):
	"""Performs an evaluation of just one sample based on sample_num and compares it to its sample label in labels"""
	# process string label from file line into numerical value
	try:
		label = labels[sample_num-1]
		label = label.split(":")[1]
		label = int(label[1:-1])
	# There is no valid label for this sample number
	except:
		return None

	print(f"\ntesting sample {sample_num}:")
	count = count_stars.main(f"samples/sample{sample_num}.jpg")
	print("labeled value - ",label)

	# percent error is the ratio of the absolute difference between measured and real, over the real
	error = (abs(count-label)/label) * 100
	print("error -",error,"%")

	# false_positives and false_negatives are dependent on the difference between the counted value and the label value
	false_positives = 0
	false_negatives = 0
	if label > count:
		false_negatives = label - count
	elif count > label:
		false_positives = count - label
	return count, label, false_positives, false_negatives, error


def main():
	"""Tests performance of count_stars.py by running it on many samples and comparing it to labels from annotation.txt. This is also capable of just running on one sample for a quick comparison if a sample number is provided via the command line."""
	try:
		fd = open(f"samples/Annotation.txt")
		labels = fd.readlines()
	except:
		print("Annotation file not found")
		return

	# if a sample number is given, just evaluate performance on that sample
	if len(sys.argv) > 1:
		sample_num = sys.argv[1]
		try:
			sample_num = int(sample_num)
		except:
			print("Sample number must be an integer")
			return

		res = test_sample(sample_num, labels)
		if res == None:
			print("There is no valid label for that sample number")
		return

	# if no sample number given, analyze all samples with valid labels and measuring false_positives, false_negatives, and error
	true_positives = 0
	total_count = 0
	cumulative_error = 0
	n_samples_tested = 0
	false_positives = 0
	false_negatives = 0
	for sample_num in range(len(labels)):
		res = test_sample(sample_num, labels)
		# skip samples without valid labels
		if res == None:
			continue
		n_samples_tested += 1
		count, label, fp, fn, err = res
		true_positives += label
		total_count += count
		false_positives += fp
		false_negatives += fn
		cumulative_error += err

	average_error = cumulative_error / n_samples_tested

	print("\n\n========= Results:")
	print("Total Count - ", total_count)
	print("False Positives -", false_positives)
	print("False Negatives -", false_negatives)
	print("Average Error - ", average_error,"%")
	print("Precision -",true_positives/(true_positives + false_positives))
	print("Recall -",true_positives/(true_positives + false_negatives),)


main()
