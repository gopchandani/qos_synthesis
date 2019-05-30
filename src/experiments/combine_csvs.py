import os
import pandas as pd

parent_directory="/home/ak7/Desktop/RTSS/RTSS_May24/raw_data"
result_directory="/home/ak7/Desktop/RTSS/RTSS_May24"
flow_ids=['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8']
#flow_ids=['f5']
cases=['bg', 'noback']


def find_and_combine_csvs(parent_directory, flow_id, case):

    for root, dirs, files in os.walk(parent_directory):

        for dir_name in dirs:
            dataframes = []

            if dir_name.find(case) >= 0:
                for sub_root,sub_dirs,sub_files in os.walk(os.path.join(parent_directory,dir_name)):

                    for sub_dir_name in sub_dirs:

                        if sub_dir_name.find("run") >= 0:
                            for sub_sub_root, sub_sub_dirs, sub_sub_files in os.walk(os.path.join(
                                                        parent_directory, dir_name, sub_dir_name
                                                            )):

                                for file in sub_sub_files:
                                    if file.endswith(".csv"):
                                        if file.find(flow_id) >= 0:
                                            print("Analysing file %s\n" % (os.path.join(parent_directory, dir_name,
                                                                                        sub_dir_name, file)))
                                            dataframe = pd.read_csv(os.path.join(parent_directory, dir_name,
                                                                                 sub_dir_name, file), header=None,
                                                                    delimiter=' ')
                                            dataframes.append(dataframe)
            if dataframes:
                final_df = pd.concat(dataframes, axis=0, ignore_index=True)
                suffix = 'BG' if (case == 'bg') else ''
                name_of_file = '_'.join([flow_id,suffix]) + '.csv'
                final_df.to_csv(os.path.join(result_directory, flow_id, name_of_file), index=False, header=False)



if __name__ == "__main__":
    for case in cases:
        for flow_id in flow_ids:
            find_and_combine_csvs(parent_directory,flow_id, case)