import dpkt, os, struct, math
from matplotlib import rcParams
from matplotlib import pyplot as plt
import numpy as np

path_root = "/home/ak7/Repositories/qos_synthesis/src/experiments/data/20181012_131415"
num_packets = 10000

def print_stats(diffs):
    print("Mean:" + str(np.mean(diffs)))
    print("Stdev:" + str(np.std(diffs)))

    print("Median:" + str(np.percentile(diffs, 50)))
    print("99th Percentile:" + str(np.percentile(diffs, 99)))
    print("99.9th Percentile:" + str(np.percentile(diffs, 99.9)))
    print("99.99th Percentile:" + str(np.percentile(diffs, 99.99)))


def plot_delay(path_root):
    """Open up a test pcap file and print out the packets"""

    path_root = path_root + '/'

    for file in os.listdir(path_root):
        if file.endswith(".pcap"):
            print('Opening ' + str(file))
            with open(path_root + file, 'rb') as f:
                pcap = dpkt.pcap.Reader(f)
                diffs = list()

                for dest_timestamp, buf in pcap:

                    with open(path_root + file.split('.')[0] + '_diff_times.csv', 'a') as f1:

                        dest_frac, dest_secs = math.modf(dest_timestamp)
                        dest_usecs = dest_frac * 1e6

                        eth = dpkt.ethernet.Ethernet(buf)
                        var = eth.pack()[50:54]
                        var2 = eth.pack()[54:58]
                        if var is None or var2 is None:
                            continue
                        else:
                            source_secs = struct.unpack(">L", var)[0]
                            source_usecs = struct.unpack(">L", var2)[0]

                            #print(source_secs, source_usecs)
                            diff_secs = dest_secs - source_secs
                            diff_usecs = dest_usecs - source_usecs

                            if (diff_usecs < 0):
                                diff_usecs = diff_usecs + (diff_secs * 1e6)

                            f1.write("%s\n" % str(diff_usecs))
                            diffs.append(diff_usecs)


                rcParams["font.family"] = "Arial"
                rcParams['font.size'] = 15
                rcParams['legend.fontsize'] = 11
                rcParams['axes.titlesize'] = 15
                rcParams['ytick.labelsize'] = 10
                rcParams['xtick.labelsize'] = 10

                # f, ax = plt.subplots(1, 1, figsize=(6.0, 4.0))
                f, ax = plt.subplots(1, 1)

                # ax.plot(diffs, '.-')
                ax.scatter(range(len(diffs)), diffs, color='k', alpha=0.7)
                plt.axhline(y=900, color='r', linestyle='-')
                ax.set_title('One-way delay for ' + file.split('_')[1])
                ax.set_xlabel('Packet Number')
                ax.set_ylabel('One way delay (us)')
                print_stats(diffs)
                plt.savefig(path_root + file.split('.')[0] + '.pdf', pad_inches=0.1, bbox_inches='tight')


if __name__ == '__main__':
     plot_delay(path_root)

