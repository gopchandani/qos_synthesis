import dpkt, os, struct, math
from matplotlib import rcParams
from matplotlib import pyplot as plt
import numpy as np
import csv

path_root = "/home/ak7/Repositories/qos_synthesis/src/experiments/data/20190527_015430nobg__rtss_scheme_run_1_100000_packets"
flow_spec = '/home/ak7/Repositories/qos_synthesis/src/experiments/flow_dict_afdx.py'
topo_spec = '/home/ak7/Repositories/qos_synthesis/src/experiments/network_configuration_hardware_afdx.py'
#num_packets = 10000

def print_stats(diffs):

    val = [ "Mean:" + str(np.mean(diffs)), "Stdev:" + str(np.std(diffs)), "Median:" + str(np.percentile(diffs, 50)),
                          "99th Percentile:" + str(np.percentile(diffs, 99)),
                          "99.9th Percentile:" + str(np.percentile(diffs, 99.9)),
                          "99.99th Percentile:" + str(np.percentile(diffs, 99.99)) ]

    output = " ".join(val)

    # print(output)
    return output


def plot_csv(path_root):
    """Open up a test pcap file and print out the packets"""

    path_root = path_root + '/'

    for file in os.listdir(path_root):
        if file.endswith(".csv"):
            print('Opening ' + str(file))
            packet_seq_no = list()
            print()
            with open(path_root + file, 'r') as f:
                # pcap = dpkt.pcap.Reader(f)
                diffs = list()
                diff_dict = dict()

                readCSV = csv.reader(f, delimiter=' ')

                for row in readCSV:
                    source_seq_no = int(row[0])
                    diff_usecs = float(row[1])
                    packet_seq_no.append(source_seq_no)
                    diffs.append(diff_usecs)
                    diff_dict[source_seq_no] = diff_usecs
                    # print("%s %s\n" %(row[0], row[1]))
                    # print("%s%s\n" %(source_seq_no, diff_dict[source_seq_no]))

                rcParams["font.family"] = "Helvetica"
                rcParams['font.size'] = 15
                rcParams['legend.fontsize'] = 11
                rcParams['axes.titlesize'] = 15
                rcParams['ytick.labelsize'] = 10
                rcParams['xtick.labelsize'] = 10

                # f, ax = plt.subplots(1, 1, figsize=(6.0, 4.0))
                f, ax = plt.subplots(1, 1)

                # ax.plot(diffs, '.-')
                #ax.scatter(range(len(diffs)), diffs, color='k', alpha=0.7)

                min_seq_num = min((diff_dict.keys()))
                max_seq_num = max((diff_dict.keys()))

                x_list_absent, y_list_absent = [], []
                x_list_primary, y_list_primary = [], []
                x_list_backup, y_list_backup = [], []

                drop = 0
                is_primary = 1

                for i in range(min_seq_num, max_seq_num + 1):
                    if i in diff_dict:
                        if is_primary == 1:# primary path or (drop == 1 and is_primary == 0)
                            x_list_primary.append(i)
                            y_list_primary.append(diff_dict[i])

                        elif (is_primary == 0): # failover path
                            x_list_backup.append(i)
                            y_list_backup.append(diff_dict[i])
                            if drop == 1:
                                drop = 0

                    else:
                        x_list_absent.append(i)
                        y_list_absent.append(2500)
                        if (drop == 0 and is_primary == 1):
                            is_primary = 0
                        elif (drop == 0 and is_primary == 0):
                            is_primary = 1
                        if drop == 0:
                            drop = 1

                ax.scatter(x_list_absent, y_list_absent, color='r', marker="x", alpha=0.7)
                ax.scatter(x_list_primary, y_list_primary, color='k', alpha=0.7)
                ax.scatter(x_list_backup, y_list_backup, color='b', alpha=0.7)

                plt.axhline(y=1200, color='g', linestyle='-', linewidth=2)
                ax.set_title('One-way delay for ' + str(file.split('_')[1]))
                ax.set_xlabel('Packet Number')
                ax.set_ylabel('One way delay (us)')

                # pdb.set_trace()
                with open(path_root + 'stats.txt', 'a') as f2:
                    f2.write("%s\n" % ((file.split('.')[0]).split('_')[0] +
                                       " : " +
                                       str(print_stats(np.asarray(diffs)))
                                       )
                             )

                # print_stats(diffs)
                plt.savefig(path_root + file.split('.')[0] + '.png', pad_inches=0.1, bbox_inches='tight')

    with open(flow_spec) as f, open(path_root + 'flow_spec.txt', "w") as g:
        g.writelines(f.readlines())

    with open(topo_spec) as f, open(path_root + 'topo_spec.txt', "w") as g:
        g.writelines(f.readlines())

if __name__ == '__main__':
     plot_csv(path_root)

