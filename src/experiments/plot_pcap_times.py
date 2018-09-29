import dpkt,os, csv, struct
import scapy
import fnmatch
import datetime
from matplotlib import rcParams
from matplotlib import pyplot as plt
import json
import numpy as np
from collections import defaultdict
import socket

path_root = "/home/ak7/Repositories/qos_synthesis/src/experiments/data/20180928_232847"
c_pattern = '_client.pcap'
s_pattern = '_server.pcap'
num_packets = 10000
flow_ids = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8']

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
        var = udp.data[968:972]
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
    client_ids=[]
    server_ids=[]
    path_root = path_root + '/'

    for fid in flow_ids:

        client_pattern = '*' + fid + c_pattern
        server_pattern = '*' + fid + s_pattern

        for file in os.listdir(path_root):
            if file.endswith(".pcap"):
                with open(path_root+file, 'rb') as f:
                    pcap = dpkt.pcap.Reader(f)

                    if fnmatch.fnmatch(file,client_pattern):
                        #client = print_packet_times(pcap)
                        print(file)
                        client, client_ids = get_packet_ids(pcap)
                        with open(path_root+file+'_client_times.csv', 'w') as f1:
                            for x in client:
                                f1.write("%s\n"%str(x))

                    elif fnmatch.fnmatch(file,server_pattern):
                        print(file)
                        #server = print_packet_times(pcap)
                        server, server_ids = get_packet_ids(pcap)
                        with open(path_root+file+'_server_times.csv', 'w') as f2:
                            for y in server:
                                f2.write("%s\n"%str(y))
                    else:
                        continue

        #print(len(client), len(server))
        #assert(len(client) == len(server))
        print(len(client_ids), len(server_ids))
        assert(len(client_ids) != 0)
        assert(len(server_ids) != 0)

        timing_dict = defaultdict(dict)

        for i, c_id in enumerate(client_ids):
            timing_dict[c_id]["client_timestamp"] = client[i]

        for j, s_id in enumerate(server_ids):
            timing_dict[s_id]["server_timestamp"] = server[j]

        weird_count = 0

        diffs = list()

        for id in timing_dict:

            if "client_timestamp" in timing_dict[id] and "server_timestamp" in timing_dict[id]:
                diff = (timing_dict[id]["server_timestamp"] - timing_dict[id]["client_timestamp"]) * 1000
                diffs.append(diff)

            if "client_timestamp" in timing_dict[id] and "server_timestamp" not in timing_dict[id]:
                diffs.append(1)

            if "client_timestamp" not in timing_dict[id] and "server_timestamp" in timing_dict[id]:
                #print(id, timing_dict[id])
                weird_count += 1

        # print(weird_count)
        # print(len(diffs))

    # for i in range(min(len(client), len(server))):
    #     diff = (server[i] - client[i])*1000
    #     diffs.append(diff)

        with open(path_root+file+'_diff_times.csv', 'w') as f1:
            for x in diffs:
                f1.write("%s\n"%str(x))

    #app_diffs, app_diffs_clipped = read_csv('f1_nobg_same_paths.csv')

        rcParams["font.family"] = "Arial"
        rcParams['font.size'] = 15
        rcParams['legend.fontsize'] = 11
        rcParams['axes.titlesize'] = 15
        rcParams['ytick.labelsize'] = 10
        rcParams['xtick.labelsize'] = 10

        #f, ax = plt.subplots(1, 1, figsize=(6.0, 4.0))
        f, ax = plt.subplots(1, 1)

        #ax.plot(diffs, '.-')
        ax.scatter(range(len(diffs)), diffs)
        plt.axhline(y=0.90, color='r', linestyle='-')
        #ax.set_title('End to End from PCAP')
        ax.set_title('One-way delay for ' + fid)
        ax.set_xlabel('Packet Number')
        ax.set_ylabel('One way delay (ms)')
        print_stats(diffs)
        plt.savefig(path_root+fid+'.png')




if __name__ == '__main__':
    plot_delay(path_root)
