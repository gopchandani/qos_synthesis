import dpkt, os, struct, math
import numpy as np

def print_stats(diffs):

    val = [ "Mean:" + str(np.mean(diffs)), "Stdev:" + str(np.std(diffs)), "Median:" + str(np.percentile(diffs, 50)),
                          "99th Percentile:" + str(np.percentile(diffs, 99)),
                          "99.9th Percentile:" + str(np.percentile(diffs, 99.9)),
                          "99.99th Percentile:" + str(np.percentile(diffs, 99.99)) ]

    output = " ".join(val)

    print(output)
    return output

def write_csv(path_root):
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

                    with open(path_root + (file.split('.')[0]).split('_')[1] + '_diff_times.csv', 'a') as f1:

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

                            f1.write("%s %s\n" %(str(source_seq_no), str(diff_usecs)))
                            diffs.append(diff_usecs)
                            packet_seq_no.append(source_seq_no)
                            diff_dict[source_seq_no] = diff_usecs

if __name__ == '__main__':
    path_root = '/home/pi'
    write_csv(path_root)
