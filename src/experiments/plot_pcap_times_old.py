import os, csv, struct, glob
import scapy
import fnmatch
import datetime
import json
import numpy as np
from collections import defaultdict
import socket
import pandas as pd

path_root = "C:\\Users\\ak7\\Desktop\\EMSOFT_Table4_Data\\RT+BG_Traffic\\20190412_185826table4_data_bg_run10\\"

def read_csv(path_root):
    for filename in os.listdir(path_root):
        if filename.endswith(".csv"):
            print("*******", filename)
            app_diff = list()
            app_diffs_clipped = []
            rowcount = 0
            with open(path_root + filename, 'r', newline='') as csvfile:
                next(csvfile)
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    print(row[3])

                    if row[3] is not None:
                        try:
                            app_diff_val = int(row[3])/1000
                            app_diff.append(app_diff_val)
                            # if app_diff > 10:
                            #     app_diffs_clipped.append(0)
                            # else:
                            #     app_diffs_clipped.append(app_diff)
                            #

                        except ValueError:
                            pass


            with open(path_root + 'stats.txt', 'a') as f2:
                f2.write("%s\n" % (filename.split('.')[0] + " : " + print_stats(app_diff)))


#

def print_stats(diffs):

    val = [ "Mean:" + str(np.mean(diffs)), "Stdev:" + str(np.std(diffs)), "Median:" + str(np.percentile(diffs, 50)),
                          "99th Percentile:" + str(np.percentile(diffs, 99)),
                          "99.9th Percentile:" + str(np.percentile(diffs, 99.9)),
                          "99.99th Percentile:" + str(np.percentile(diffs, 99.99)) ]

    output = " ".join(val)

    #print(output)
    return output


if __name__ == '__main__':
    # plot_delay(path_root)
    read_csv(path_root)