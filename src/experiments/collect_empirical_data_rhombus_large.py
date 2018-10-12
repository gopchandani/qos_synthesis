import paramiko
import os
import numpy as np
import threading
import csv
import datetime
import time
from collections import defaultdict
from src.experiments.plot_pcap_times_pktgen import plot_delay
from src.experiments.flow_dict import all_flows as flows
from src.experiments.topo_dict import host_ip

from src.synthesis.synthesize_simple_backup_flows import SynthesizeSimpleBackupFlows
from src.experiments.network_configuration_hardware_nsdi import NetworkConfigurationHardwareNsdi

#client_process = "`echo $HOME`/Repositories/qos_synthesis/traffic_generation/udp_client/client"
#server_process = "`echo $HOME`/Repositories/qos_synthesis/traffic_generation/udp_server/server"
#should_nice = True

pktgen_script = "sudo taskset 0x1 sudo `echo $HOME`/Repositories/linux/samples/pktgen/pktgen_sample01_simple.sh"
packet_size_in_bytes = 1024
num_packets = 100000
num_threads = 1
burst = 0


def run_cmd_via_paramiko(IP, command, port=22, username='pi', password='raspberry'):

    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()

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

def run_tcpdump(flow_num, is_client, num_packets):
    file_name = flow_num +'_client.pcap' if is_client else flow_num +'_server.pcap'
    output_file = 'tcpdump_' + file_name
    tcpdump_command = 'sudo taskset 0x4 sudo nice --20 tcpdump -U -i eth0 -B 30720 -c ' + str(num_packets) + ' udp dst portrange 10000-10007 -w ' + output_file
    return tcpdump_command

def client_command(server_ip, num_packets, flow_rate_in_Mbps, port_no):

    budget = (1E9 * 8) / int (1000 * float(flow_rate_in_Mbps))
    client_command = ' '.join([client_process, server_ip, num_packets, str(int(budget)), str(port_no)])
    if should_nice == True:
        client_command = 'sudo nice --20 ' + client_command

    print(client_command)
    return client_command

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

    command = ' '.join([pktgen_script, '-vx', '-i', 'eth0',
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

def server_command(port_no, num_packets, flow_num, is_background, is_same):
    file_name = '_'.join([flow_num, is_background, is_same])
    output_file = '.'.join([file_name, 'csv'])
    server_command = ' '.join([server_process, port_no, num_packets]) + ' ' + output_file
    if should_nice == True:
        server_command = 'sudo nice --20 ' + server_command + ' &'

    print(server_command)
    return server_command

def update_traffic_repo():
    for client in host_ip:
        print(run_cmd_via_paramiko(host_ip[client][1], "cd Repositories/qos_synthesis; cd traffic_generation/;"
                                                       "cd udp_client/; make clean;"
                                                       "cd ../udp_server/; make clean;"
                                                       "cd ../../;"
                                                       "git pull;"))

def compile_traffic_repo():
    for client in host_ip:
        print(run_cmd_via_paramiko(host_ip[client][1], "cd Repositories/qos_synthesis/traffic_generation/; "
                                                       "cd udp_server/; make; cd ../udp_client/; make;"))

def clean_client_server():
    for client in host_ip:
        #print(run_cmd_via_paramiko(host_ip[client][1], "sudo pkill -x client; sudo pkill -x server; sudo rm *.csv; sudo rm *.pcap"))
        print(run_cmd_via_paramiko(host_ip[client][1], "sudo pkill -x pktgen_sample01; sudo pkill -x tcpdump; sudo rm *.pcap"))
        #print(run_cmd_via_paramiko(host_ip[client][1], "sudo /home/pi/scripts/powersave_governor.sh"))

def update_pi_scripts():
    for client in host_ip:
        print(run_cmd_via_paramiko(host_ip[client][1], "cd scripts/; rm -rf *; git init; git remote add origin "
                                                       "https://github.com/gopchandani/qos_synthesis.git; git pull;"
                                                       "git checkout pi_scripts "))

def download_linux_insert_pktgen_driver():
    for client in host_ip:
        print(host_ip[client][1])
        print(run_cmd_via_paramiko(host_ip[client][1], "cd Repositories/; git clone --depth=1 https://github.com/raspberrypi/linux.git;"))
        print(run_cmd_via_paramiko(host_ip[client][1], "sudo insmod /lib/modules/`uname -r`/kernel/net/core/pktgen.ko "))

def start_all_flows_simultaneously(packet_size_in_bytes, num_packets, num_threads, burst):

    tcpdump_jobs = []
    rt_traffic_jobs = []

    for flow in flows:
        if flow["type"] == "data":

            print()
            print(host_ip[flow["client"]][0], '------->', host_ip[flow["server"]][0])
            tcpdump_server_thread = threading.Thread(target=run_cmd_via_paramiko, args=(host_ip[flow["server"]][1],
                                                                                run_tcpdump(flow["id"],
                                                                                            0, num_packets)))
            tcpdump_server_thread.start()
            tcpdump_jobs.append(tcpdump_server_thread)

            time.sleep(1.0)
            print('Starting Client')
            client_thread = threading.Thread(target=run_cmd_via_paramiko, args=(host_ip[flow["client"]][1],
                                                                                client_command_pktgen(
                                                                                    packet_size_in_bytes,
                                                                                    host_ip[flow["server"]][0],
                                                                                    host_ip[flow["server"]][2],
                                                                                    num_threads,
                                                                                    burst,
                                                                                    flow['rate'],
                                                                                    num_packets)
                                                                                )
                                             )
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

    print('tcpdumps have finished')


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
    paths = input('Is it same or different paths?')

    is_background = 'bg' if background_traffic else 'nobg'
    is_same = 'same_paths' if paths else 'diff_paths'

    start_all_flows_simultaneously(packet_size_in_bytes, num_packets, num_threads, burst)
    mydir = get_rhombus_data_pscp('_'.join([is_background, is_same]))
    plot_delay(mydir)

    return 0


# def get_rhombus_data(file_suffix):
#     local_data_location = datetime.datetime.today().strftime('%Y-%m-%d')
#     for f in flows:
#         remote_filepath = f["data_loc"] + f["id"] + '_' + file_suffix + ".csv"
#         cmd = "scp " + f["user"] + "@" + host_ip[f["server"]][1] + ":" + remote_filepath + " " + local_data_location
#         os.system(cmd)


def get_rhombus_data_pscp(file_suffix):

    mydir = os.path.join(os.getcwd() + '/data/', datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    os.makedirs(mydir)

    for f in flows:
        if f["type"] == "data":
            tcpdump_file_server = f["data_loc"] + 'tcpdump_' + f["id"] + '_server' + '.pcap'
            get_tcpdump_server = "pscp " + "-pw raspberry " + f["user"] + "@" + host_ip[f["server"]][1] + ":" + tcpdump_file_server + " " + mydir + '/'

            print(get_tcpdump_server)
            os.system(get_tcpdump_server)

        else:
            continue

    return mydir

def reject_outliers(data, m=2):
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
        print("Flow: %s, #-Samples: %s, Avg: %s, Stdev: %s, 50th Percentile: %s, 99th Percentile: %s, 99.9th Percentile: %s" % (
            flow,
            len(output[flow]),
            np.mean(output[flow]),
            np.std(reject_outliers(np.asarray(output[flow]))),
            np.percentile(output[flow], 50),
            np.percentile(output[flow], 99),
            np.percentile(output[flow], 99.9)
        ))


if __name__ == "__main__":
    #download_linux_insert_pktgen_driver()
    main()
