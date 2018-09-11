import dpkt,os, csv, struct
import scapy
import fnmatch
import datetime
from matplotlib import pyplot as plt
import json
import numpy as np
from collections import defaultdict
import socket

path_root = "/Users/Kashinath/Repositories/qos_synthesis/src_multiplex_synthetic/20180911_140555/"
#directory_pattern="FF*"
client_pattern = '*client.pcap'
server_pattern = '*server.pcap'
num_packets = 100000

def print_packet_times(pcap):
    # For each packet in the pcap process the contents
    times = []
    for timestamp in pcap:
        times.append(timestamp[0])

    return times


def get_packet_ids(pcap):
    timestamps = []
    packet_ids = []

    for ts, buf in pcap:
        timestamps.append(ts)

        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        udp = ip.data
        var = udp.data[0:4]
        #print(type(var), type(var[0]))
        uvar = struct.unpack("<L", var)[0]
        packet_ids.append(uvar)

    return timestamps, packet_ids

def read_csv(filename):

    app_diffs = []
    app_diffs_clipped = []
    rowcount = 0
    with open(path_root+filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rowcount = rowcount + 1
            if rowcount <= (num_packets + 1):

                if row[" One-way delay(ns)"] is not None:
                    try:
                        app_diff = int(row[" One-way delay(ns)"])/1000000

                        if app_diff > 10:
                            app_diffs_clipped.append(0)
                        else:
                            app_diffs_clipped.append(app_diff)

                        app_diffs.append(app_diff)
                    except ValueError:
                        pass

    return app_diffs, app_diffs_clipped


def print_stats(diffs):
    print("Mean:" + str(np.mean(diffs)))
    print("Stdev:" + str(np.std(diffs)))

    print("Median:" + str(np.percentile(diffs, 50)))
    print("99th Percentile:" + str(np.percentile(diffs, 99)))
    print("99.9th Percentile:" + str(np.percentile(diffs, 99.9)))
    print("99.99th Percentile:" + str(np.percentile(diffs, 99.99)))


def plot_delay(path_root):
    """Open up a test pcap file and print out the packets"""
    client=[]
    server=[]
    diffs = []
    client_ids=[]
    server_ids=[]
    path_root = path_root + '/'


    for file in os.listdir(path_root):
        if file.endswith(".pcap"):
            with open(path_root+file, 'rb') as f:
                pcap = dpkt.pcap.Reader(f)

                if fnmatch.fnmatch(file,client_pattern):
                    #client = print_packet_times(pcap)
                    client, client_ids = get_packet_ids(pcap)
                    with open(path_root+'client_times.csv', 'w') as f1:
                        for x in client:
                            f1.write("%s\n"%str(x))
                else:
                    #server = print_packet_times(pcap)
                    server, server_ids = get_packet_ids(pcap)
                    with open(path_root+'server_times.csv', 'w') as f2:
                        for y in server:
                            f2.write("%s\n"%str(y))

    print(len(client), len(server))
    #assert(len(client) == len(server))

    timing_dict = defaultdict(dict)

    for i, c_id in enumerate(client_ids):
        timing_dict[c_id]["client_timestamp"] = client[i]

    for i, s_id in enumerate(server_ids):
        timing_dict[s_id]["server_timestamp"] = server[i]

    weird_count = 0

    for id in timing_dict:

        if "client_timestamp" in timing_dict[id] and "server_timestamp" in timing_dict[id]:
            diff = (timing_dict[id]["server_timestamp"] - timing_dict[id]["client_timestamp"]) * 1000
            diffs.append(diff)

        if "client_timestamp" in timing_dict[id] and "server_timestamp" not in timing_dict[id]:
            diffs.append(1)

        if "client_timestamp" not in timing_dict[id] and "server_timestamp" in timing_dict[id]:
            print(id, timing_dict[id])
            weird_count += 1

    print(weird_count)
    print(len(diffs))

    # for i in range(min(len(client), len(server))):
    #     diff = (server[i] - client[i])*1000
    #     diffs.append(diff)

    with open(path_root+'diff_times.csv', 'w') as f1:
        for x in diffs:
            f1.write("%s\n"%str(x))

    #app_diffs, app_diffs_clipped = read_csv('f1_nobg_same_paths.csv')


    plt.subplot(1, 1, 1)
    plt.plot(diffs, '.-')
    plt.title('End to End from PCAP')
    plt.xlabel('Packet Number')
    plt.ylabel('One way delay (ms)')

    plt.subplots_adjust(hspace=1.0)

    print_stats(diffs)

    plt.show()


if __name__ == '__main__':
    plot_delay(path_root)
