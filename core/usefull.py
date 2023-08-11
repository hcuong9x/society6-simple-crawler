import csv


def get_data_in_file(fileName, skip_header=1):
	data = []
	with open(fileName) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for i, row in enumerate(csv_reader):
			if skip_header:
				if i == 0:  # skip header row
					continue
			data.append(row)

	return data