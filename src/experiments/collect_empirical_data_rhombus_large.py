import paramiko
import os
import numpy as np
import threading
import csv
import datetime
import time
from collections import defaultdict
from src.experiments.plot_pcap_times_pktgen import plot_delay
from src.experiments.flow_dict_afdx import all_flows as flows
from src.experiments.topo_dict_afdx import host_ip

from src.synthesis.synthesize_simple_backup_flows import SynthesizeSimpleBackupFlows
from src.experiments.network_configuration_hardware_afdx import NetworkConfigurationHardwareNsdi

# should_nice = True

# Pi has 4 cores
# Traffic generation on core 0,
# PTP Daemon on core 1 and,
# tcpdump runs on core 2

pktgen_script = "sudo taskset 0x1 sudo `echo $HOME`/Repositories/linux/samples/pktgen/pktgen_sample01_simple.sh"
packet_size_in_bytes = 1024
num_packets = 10000
num_threads = 4
burst = 0


def run_cmd_via_paramiko(IP, command, port=22, username='pi', password='raspberry'):

    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()

    if IP == host_ip["dot250"][1] or IP == host_ip["dot123"][1]:
        username = 'iti'
        password = 'csl440'

    s.connect(IP, port, username, password)
    (stdin, stdout, stderr) = s.exec_command(command)

    output = list(stdout.readlines())
    s.close()
    return output


'''
    flow_rate_in_MBps = (flow_rate_in_Mbps/8)
    flow_rate_in_kBps = flow_rate_in_MBps * 1E3
    packet_size = 1kB
    flow_rate = (flow_rate_in_kBps) packets per second
    time between packets = 1 / flow_rate

    sudo nice --20 ./udp_client/client 192.168.1.40 1000 97660 10000
    sudo nice --20 ./udp_server/server 10010 1000 > f11_nobg_same_paths.csv

'''

def run_tcpdump(flow_num, is_client, num_packets, interface_name):
    file_name = flow_num +'_client.pcap' if is_client else flow_num +'_server.pcap'
    output_file = 'tcpdump_' + file_name

    tcpdump_command = 'sudo taskset 0x4 sudo nice --20 tcpdump -U -i ' + interface_name + \
                      ' -B 307200 -c ' + str(num_packets) + ' udp dst portrange 10000-10011 -w ' + output_file

    print(tcpdump_command)

    return tcpdump_command

# def setup_sed(port_number):
#     TODO:
#     for client in host_ip:
#         command1 = "sed -i '27s/.*/\[ -z \"\$DELAY\" \] \&\& DELAY=\"1000\"/' ~/Repositories/linux/samples/pktgen/pktgen_sample01_simple.sh"
#         command2 = "sed -i '48i pg_set $DEV \"udp_dst_min '" + str(port_number) + "'\"\npg_set $DEV \"udp_dst_max '" + str(port_number) + "'\"' ~/Repositories/linux/samples/pktgen/pktgen_sample01_simple.sh"
#         command = command1 + ';' + command2
#         print(run_cmd_via_paramiko(host_ip[client][1], command))
#
#     return command

def client_command_pktgen(packet_size_in_bytes, server_ip, server_mac, num_threads, burst, flow_rate_in_Mbps, num_packets):

    inter_packet_time_in_ns = int((packet_size_in_bytes * 8 * 1000)/(flow_rate_in_Mbps))

    if server_ip == host_ip["dot123"][0]:
        eth_interface_name = 'enp0s25'
    else:
        eth_interface_name = 'eth0'

    command = ' '.join([pktgen_script, '-vx', '-i', str(eth_interface_name),
                        '-s', str(packet_size_in_bytes),
                        '-d', str(server_ip),
                        '-m', str(server_mac),
                        '-t', str(num_threads),
                        '-b', str(burst),
                        '-g', str(inter_packet_time_in_ns),
                        '-n', str(num_packets)
                        ])

    print(command)
    return command


def clean_client_server():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "sudo pkill -x pktgen_sample01; "
                                                       "sudo pkill -x tcpdump; "
                                                       "sudo rm *.pcap"))


def reinstall_pi_scripts():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "rm -rf scripts/; mkdir scripts/ ;cd scripts/; "
                                                       "git clone -b pi_scripts --single-branch "
                                                       "https://github.com/gopchandani/qos_synthesis.git .; "))

def update_pi_scripts():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "cd scripts/; git pull"))

def run_startup_scripts():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "sudo scripts/arp_table_fix.sh;"
                                                       "sudo scripts/powersave_governor.sh;"
                                                       "sudo scripts/set_os_network_buffers"))


def install_vim_tcpdump():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "sudo apt install tcpdump -y;"
                                                       "sudo apt install vim -y;"))


def download_linux_insert_pktgen_driver():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "cd Repositories/; "
                                                       "git clone --depth=1 https://github.com/raspberrypi/linux.git;"))
        print(run_cmd_via_paramiko(host_ip[client][1], "sudo insmod "
                                                       "/lib/modules/`uname -r`/kernel/net/core/pktgen.ko "))

def start_all_flows_simultaneously(packet_size_in_bytes, num_packets, num_threads, burst):

    tcpdump_jobs = []
    rt_traffic_jobs = []

    for flow in flows:
        if flow["type"] == "data":

            print()
            print(host_ip[flow["client"]][0], '------->', host_ip[flow["server"]][0])

            if flow["server"] == "dot123":
                eth_interface_name = 'enp0s31f6'
                #num_packets = 700000
            else:
                eth_interface_name = 'eth0'


            tcpdump_server_thread = threading.Thread(target=run_cmd_via_paramiko,
                                                     args=(
                                                         host_ip[flow["server"]][1],
                                                         run_tcpdump(flow["id"],0, num_packets, eth_interface_name)))

            tcpdump_server_thread.start()
            tcpdump_jobs.append(tcpdump_server_thread)

            time.sleep(1.0)
            print('Starting Client')
            client_thread = threading.Thread(target=run_cmd_via_paramiko,
                                                    args=(
                                                        host_ip[flow["client"]][1],
                                                        client_command_pktgen(
                                                        packet_size_in_bytes,
                                                        host_ip[flow["server"]][0],
                                                        host_ip[flow["server"]][2],
                                                        num_threads,
                                                        burst,
                                                        flow['rate'],
                                                        num_packets)))

            client_thread.setDaemon(True)
            rt_traffic_jobs.append(client_thread)

    for job in rt_traffic_jobs:
        job.start()

    print('Flows are running now')

    for client_thread in rt_traffic_jobs:
        client_thread.join()

    print('Clients have finished sending the packets')

    time.sleep(2.0)

    for h in host_ip:
        run_cmd_via_paramiko(host_ip[h][1], 'sudo killall tcpdump')

    print('tcpdump\'s have finished')


def main():

    clean_client_server()
    print("Starting")
    nc = NetworkConfigurationHardwareNsdi()
    nc.setup_network_configuration()

    print('network configuration done')
    params = {"nc": nc,
              "flows": flows}

    ssbf = SynthesizeSimpleBackupFlows(params)
    ssbf.compute_switch_configurations()
    ssbf.trigger()

    background_traffic = input('Is there a background flow?')
    paths = input('Is it intuitive(enter 1) or non-intuitive path(enter 0) experiment?')

    is_background = 'bg' if background_traffic else 'nobg'
    is_same = 'intuitive_paths' if paths else 'nonintuitive_paths'

    time.sleep(120.0)
    start_all_flows_simultaneously(packet_size_in_bytes, num_packets, num_threads, burst)
    mydir = get_rhombus_data_pscp('_'.join([is_background, is_same]))
    plot_delay(mydir)

    return 0


def get_rhombus_data_pscp(file_suffix):

    mydir = os.path.join(os.getcwd() + '/data/', datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+file_suffix)
    os.makedirs(mydir)

    for f in flows:
        # We only get end to end deplays for Real-time traffic
        if f["type"] == "data":

            if f["server"] == "dot123":
                password = "csl440"
            else:
                password = "raspberry"

            tcpdump_file_server = f["data_loc"] + 'tcpdump_' + f["id"] + '_server' + '.pcap'
            get_tcpdump_server = "pscp " + "-pw "+ password + " " + \
                                 f["user"] + "@" + host_ip[f["server"]][1] + \
                                 ":" + tcpdump_file_server + " " + mydir + '/'

            print(get_tcpdump_server)
            os.system(get_tcpdump_server)

        else:
            continue

    return mydir


def reject_outliers(data, m=2):

    # Statistical Witchcraft -- Use with CAUTION
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def processed_expt_output(directory):

    output = defaultdict(list)

    for f in os.listdir(directory):
        with open(directory + '/' + f) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row[" One-way delay(ns)"] is not None:
                    try:
                        output[f].append(int(row[" One-way delay(ns)"]))
                    except ValueError:
                        pass

    for flow in output:
        print("Flow: %s, "
              "#-Samples: %s, "
              "Avg: %s, "
              "Stdev: %s, "
              "50th Percentile: %s, "
              "99th Percentile: %s, "
              "99.9th Percentile: %s" % (
                flow,
                len(output[flow]),
                np.mean(output[flow]),
                np.std(reject_outliers(np.asarray(output[flow]))),
                np.percentile(output[flow], 50),
                np.percentile(output[flow], 99),
                np.percentile(output[flow], 99.9)
            )
        )


if __name__ == "__main__":

    main()
    # run_startup_scripts()
    # reinstall_pi_scripts()
    # download_linux_insert_pktgen_driver()

