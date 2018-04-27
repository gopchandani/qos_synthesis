import csv
import json
import glob


periods_str = ['1000ms', '100ms']
num_switches_strs = ['1', '2', '3', '4']
payloads_strs = ['256B', '512B', '1024B', '1408B']

data_root = 'data/'


def convert_csv_to_process_time_list(period_str, num_switches_str, payload_str):

    processing_time_list = []
    csv_file_path_dir = data_root + period_str + '/' + num_switches_str + '/' + payload_str + '/'

    for csv_file_path in glob.iglob(csv_file_path_dir + '*.csv'):

        with open(csv_file_path, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            field_of_interest = reader.fieldnames[3]
            next(reader)
            for row in reader:
                val = float(row[field_of_interest])/1000

                if val > 10000:
                    print "Ignoring anomalous high value:", val, "in:", csv_file_path
                else:
                    processing_time_list.append(val)

    return processing_time_list


def get_data_dict():

    # Initialize the data dictionary
    data_dict = dict()
    for period_str in periods_str:
        data_dict[period_str] = dict()
        for num_switches_str in num_switches_strs:
            data_dict[period_str][num_switches_str] = dict()

    # Populate the dictionary using CSV file
    for period_str in periods_str:
        for num_switches_str in num_switches_strs:
            for payload_str in payloads_strs:
                data_dict[period_str][num_switches_str][payload_str] = \
                    convert_csv_to_process_time_list(period_str, num_switches_str, payload_str)

                # Sanity check
                if period_str == '1000ms' and num_switches_str == '1' and payload_str == '1408B':
                    pass

    return data_dict

data_dict = get_data_dict()

# Dump the json file
with open(data_root + 'data.json', 'w') as outfile:
    json.dump(data_dict, outfile, indent=2)
