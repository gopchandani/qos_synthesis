import dpkt, os, struct, math
from matplotlib import rcParams
from matplotlib import pyplot as plt
import numpy as np
import itertools

path_root = "/home/ak7/Repositories/qos_synthesis/src/experiments/data/20190206_035131bg_intuitive_paths"
flow_spec = '/home/ak7/Repositories/qos_synthesis/src/experiments/flow_dict.py'
topo_spec = '/home/ak7/Repositories/qos_synthesis/src/experiments/network_configuration_hardware_nsdi.py'
num_packets = 10000

def print_stats(diffs):

    val = [ "Mean:" + str(np.mean(diffs)), "Stdev:" + str(np.std(diffs)), "Median:" + str(np.percentile(diffs, 50)),
                          "99th Percentile:" + str(np.percentile(diffs, 99)),
                          "99.9th Percentile:" + str(np.percentile(diffs, 99.9)),
                          "99.99th Percentile:" + str(np.percentile(diffs, 99.99)) ]

    output = " ".join(val)

    print(output)
    return output


    # print("Mean:" + str(np.mean(diffs)))
    # print("Stdev:" + str(np.std(diffs)))
    #
    # print("Median:" + str(np.percentile(diffs, 50)))
    # print("99th Percentile:" + str(np.percentile(diffs, 99)))
    # print("99.9th Percentile:" + str(np.percentile(diffs, 99.9)))
    # print("99.99th Percentile:" + str(np.percentile(diffs, 99.99)))


def plot_delay(path_root):
    """Open up a test pcap file and print out the packets"""

    path_root = path_root + '/'

    for file in os.listdir(path_root):
        if file.endswith(".pcap"):
            packet_seq_no = list()
            print()
            print('Opening ' + str(file))
            with open(path_root + file, 'rb') as f:
                pcap = dpkt.pcap.Reader(f)
                diffs = list()
                diff_dict = dict()

                for dest_timestamp, buf in pcap:

                    with open(path_root + file.split('.')[0] + '_diff_times.csv', 'a') as f1:

                        dest_frac, dest_secs = math.modf(dest_timestamp)
                        dest_usecs = dest_frac * 1e6

                        eth = dpkt.ethernet.Ethernet(buf)
                        seq_no = eth.pack()[46:50]
                        var = eth.pack()[50:54]
                        var2 = eth.pack()[54:58]

                        if var is None or var2 is None:
                            continue
                        else:
                            source_secs = struct.unpack(">L", var)[0]
                            source_usecs = struct.unpack(">L", var2)[0]
                            source_seq_no = struct.unpack(">L", seq_no)[0]
                            # print(source_seq_no)

                            # print(source_secs, source_usecs)
                            diff_secs = dest_secs - source_secs
                            diff_usecs = dest_usecs - source_usecs + (diff_secs * 1e6)

                            # if (diff_usecs < 0):
                            #     diff_usecs = diff_usecs + (diff_secs * 1e6)

                            f1.write("%s\n" % str(diff_usecs))
                            diffs.append(diff_usecs)
                            packet_seq_no.append(source_seq_no)
                            diff_dict[source_seq_no] = diff_usecs

                rcParams["font.family"] = "Arial"
                rcParams['font.size'] = 15
                rcParams['legend.fontsize'] = 11
                rcParams['axes.titlesize'] = 15
                rcParams['ytick.labelsize'] = 10
                rcParams['xtick.labelsize'] = 10

                # f, ax = plt.subplots(1, 1, figsize=(6.0, 4.0))
                f, ax = plt.subplots(1, 1)

                # ax.plot(diffs, '.-')
                #ax.scatter(range(len(diffs)), diffs, color='k', alpha=0.7)

                min_seq_num = min(diff_dict.keys())
                max_seq_num = max(diff_dict.keys())

                x_list_present, y_list_present = [], []
                x_list_absent, y_list_absent = [], []

                for i in range(min_seq_num, max_seq_num + 1):
                    if i in diff_dict:
                        x_list_present.append(i)
                        y_list_present.append(diff_dict[i])
                    else:
                        x_list_absent.append(i)
                        y_list_absent.append(2500)

                ax.scatter(x_list_absent, y_list_absent, color='r', marker="x", alpha=0.7)
                ax.scatter(x_list_present, y_list_present, color='k', alpha=0.7)

                plt.axhline(y=1200, color='r', linestyle='-')
                ax.set_title('One-way delay for ' + file.split('_')[1])
                ax.set_xlabel('Packet Number')
                ax.set_ylabel('One way delay (us)')

                with open(path_root + 'stats.txt', 'a') as f2:
                    f2.write("%s\n" % ((file.split('.')[0]).split('_')[1] + " : " + print_stats(diffs)))

                # print_stats(diffs)


                plt.savefig(path_root + file.split('.')[0] + '.pdf', pad_inches=0.1, bbox_inches='tight')

    with open(flow_spec) as f, open(path_root + 'flow_spec.txt', "w") as g:
        g.writelines(f.readlines())

    with open(topo_spec) as f, open(path_root + 'topo_spec.txt', "w") as g:
        g.writelines(f.readlines())

if __name__ == '__main__':
     plot_delay(path_root)

