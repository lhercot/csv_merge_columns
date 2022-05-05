import re
import csv
from os import walk

OUTPUT_FILE = "output.csv"
PORT_NUMBER_REGEX = ".*?port([0-9]+?).csv"
PORT_NAME_REGEX = ".*?(port[0-9]+?).csv"

def sort_by_port_id(filename):
    return int(re.search(PORT_NUMBER_REGEX, filename.lower()).group(1))

csv_files = []
filenames = next(walk('./'), (None, None, []))[2]  # [] if no file
for filename in filenames:
    if re.search(PORT_NUMBER_REGEX, filename.lower()):
        csv_files.append(filename)
csv_files.sort(key=sort_by_port_id)
print("File to be processed: " + ', '.join(csv_files))

new_rows = {}
for csv_file in csv_files:
    with open(csv_file, newline='') as csv_file_object:
        csv_dict_reader = csv.DictReader(csv_file_object, fieldnames=list(range(100)))
        for row in csv_dict_reader:
            header_name = re.search(PORT_NAME_REGEX, csv_file.lower()).group(1)
            if header_name not in new_rows:
                new_rows[header_name] = [row[1]]
            else:
                new_rows[header_name].append(row[1])

max_length = 0
for header, column_data in new_rows.items():
    if len(column_data) > max_length:
        max_length = len(column_data)

with open(OUTPUT_FILE, 'w', newline='') as merged_csv:
    csv_dict_writer = csv.DictWriter(merged_csv, new_rows.keys())
    csv_dict_writer.writeheader()
    for i in range(max_length):
        row_data = {}
        for header, column_data in new_rows.items():
            row_data[header] = column_data[i]

        csv_dict_writer.writerow(row_data)

print("Processing finished.")