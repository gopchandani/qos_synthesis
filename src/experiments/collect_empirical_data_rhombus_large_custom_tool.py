import paramiko
import os
import numpy as np
import threading
import csv
import datetime
import time
from collections import defaultdict
# from src.experiments.plot_pcap_times_pktgen import plot_delay
from src.experiments.plot_cdf_hist_from_csv import read_csv
from src.experiments.flow_dict_afdx import all_flows as flows
from src.experiments.topo_dict_afdx import host_ip
# from src.experiments.topo_dict import host_ip
# from src.experiments.flow_dict import all_flows as flows

from src.synthesis.synthesize_simple_backup_flows import SynthesizeSimpleBackupFlows
from src.experiments.network_configuration_hardware_afdx import NetworkConfigurationHardwareNsdi
#from src.experiments.network_configuration_hardware_nsdi import NetworkConfigurationHardwareNsdi

# should_nice = True

# Pi has 4 cores
# Traffic generation on core 0,
# PTP Daemon on core 1 and,
# tcpdump runs on core 2

pktgen_script = "sudo taskset 0x1 sudo `echo $HOME`/Repositories/linux/samples/pktgen/pktgen_sample01_simple.sh"
packet_size_in_bytes = 1024
num_packets = 100000 # 100k packets for our experiments
burst = 0

client_script = "sudo taskset 0x1 sudo `echo $HOME`/Repositories/qos_synthesis/traffic_generation/udp_client/client"
server_script = "sudo taskset 0x4 sudo `echo $HOME`/Repositories/qos_synthesis/traffic_generation/udp_server/server"
packet_gap_in_ns = 1000000 # 1 ms the packet gap in AFDX spec

# Background to RT Traffic
speedup_factor = 5


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


# def setup_sed(port_number):
#     TODO:
#     for client in host_ip:
#         command1 = "sed -i '27s/.*/\[ -z \"\$DELAY\" \] \&\& DELAY=\"1000\"/' ~/Repositories/linux/samples/pktgen/pktgen_sample01_simple.sh"
#         command2 = "sed -i '48i pg_set $DEV \"udp_dst_min '" + str(port_number) + "'\"\npg_set $DEV \"udp_dst_max '" + str(port_number) + "'\"' ~/Repositories/linux/samples/pktgen/pktgen_sample01_simple.sh"
#         command = command1 + ';' + command2
#         print(run_cmd_via_paramiko(host_ip[client][1], command))
#
#     return command


# Haven't parameterized packet size yet
def client_command(server_ip, num_packets, packet_gap_in_ns, port_num):

    command = ' '.join([client_script, str(server_ip)
                        , str(num_packets)
                        , str(packet_gap_in_ns)
                        , str(port_num)
                        ])

    print(command)
    return command

def server_command(port_num, num_packets, file_name):

    command = ' '.join([server_script
                        , str(port_num)
                        , str(num_packets)
                        , '>'
                        , str(file_name)
                        ])

    print(command)
    return command


def clean_client_server():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "sudo pkill -x pktgen_sample01; "
                                                       "sudo pkill -x tcpdump; "
                                                       "sudo rm *.pcap"))

def kill_ptp_start_again():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "source ~/.bashrc;"))

def update_arp_tables():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "cd scripts; sudo ./arp_table_fix.sh;"))

def is_ptp_running():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "ps -el | grep ptp"))

def reboot_hosts():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "sudo reboot;"))

def ping_hosts():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "echo hello;"))

def put_in_performance_mode():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "sudo /home/pi/scripts/performance_governor.sh;"))

def put_in_powersave_mode():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "sudo /home/pi/scripts/powersave_governor.sh;"))

def install_ptp_commands_in_hosts():
    for flow in flows:
        print(host_ip[flow["client"]][0], host_ip[flow["server"]][0])
        # Server command
        c_c = 'sudo ptpd2 --interface eth0 --slaveonly --unicast -u ' + host_ip[flow["server"]][0] + \
                             ' --debug --foreground --verbose'
        client_ptp_command = 'echo ' + c_c + ' >> .bashrc'
        print(client_ptp_command)

        print(run_cmd_via_paramiko(host_ip[flow["client"]][1], client_ptp_command))

        s_c = 'sudo ptpd2 --interface eth0 --masteronly --unicast -u ' + host_ip[flow["client"]][0] + \
                             ' --debug --foreground --verbose'
        server_ptp_command = 'echo ' + s_c + ' >> .bashrc'
        print(server_ptp_command)

        print(run_cmd_via_paramiko(host_ip[flow["server"]][1], server_ptp_command))


def reinstall_pi_scripts():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "rm -rf scripts/; mkdir scripts/ ;cd scripts/; "
                                                       "git clone -b pi_scripts --single-branch "
                                                       "https://github.com/gopchandani/qos_synthesis.git .; "))

def update_pi_scripts():
    for client in host_ip:
        print(host_ip[client][0])
        print(run_cmd_via_paramiko(host_ip[client][1], "cd scripts/; git pull; sudo ./arp_table_fix.sh;"))

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

def start_all_flows_simultaneously(num_packets):

    server_jobs = []
    rt_traffic_jobs = []

    for flow in flows:
        if flow["type"] == "data":

            print()
            print(host_ip[flow["client"]][0], '------->', host_ip[flow["server"]][0])


            server_thread = threading.Thread(target=run_cmd_via_paramiko,
                                                     args=(
                                                         host_ip[flow["server"]][1],
                                                         server_command(flow["port"], num_packets, '.'.join([flow["id"], 'csv']))
                                                    )
                                            )

            server_thread.start()
            server_jobs.append(server_thread)

            time.sleep(1.0)
            print('Starting Client')
            client_thread = threading.Thread(target=run_cmd_via_paramiko,
                                                    args=(
                                                        host_ip[flow["client"]][1],
                                                        client_command(
                                                        host_ip[flow["server"]][0],
                                                        num_packets,
                                                        packet_gap_in_ns,
                                                        flow["port"]
                                                        )
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

    # for h in host_ip:
    #     run_cmd_via_paramiko(host_ip[h][1], 'sudo killall tcpdump')

    print('servers\'s have finished')


def main():

    clean_client_server()
    print("Starting")
    nc = NetworkConfigurationHardwareNsdi()
    nc.setup_network_configuration()

    print('network configuration done')
    params = {"nc": nc,
              "flows": flows}

    ssbf = SynthesizeSimpleBackupFlows(params)
    print('---- SynthesizeSimpleBackupFlows done')
    ssbf.compute_switch_configurations()
    print('---- compute_switch_configurations done')
    ssbf.trigger()
    print('---- trigger done')

    # background_traffic = input('Is there a background flow?')
    # paths = input('Is it intuitive(enter 1) or non-intuitive path(enter 0) experiment?')

    # is_background = 'bg' if background_traffic else 'nobg'
    # is_same = 'intuitive_paths' if paths else 'nonintuitive_paths'

    is_background = 'table4_data'
    is_same = ''

    time.sleep(120.0)
    start_all_flows_simultaneously(num_packets)
    mydir = get_rhombus_data_pscp('_'.join([is_background, is_same]))
    read_csv(mydir)

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

            server_file = f["data_loc"] + f["id"] + '.csv'
            get_server_file = "pscp " + "-pw "+ password + " " + \
                                 f["user"] + "@" + host_ip[f["server"]][1] + \
                                 ":" + server_file + " " + mydir + '/'

            print(get_server_file)
            os.system(get_server_file)

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

    # kill_ptp_start_again()
    #put_in_performance_mode()
    # put_in_powersave_mode()
    main()

    # is_ptp_running()
    # run_startup_scripts()
    # reinstall_pi_scripts()
    # update_pi_scripts()
    # install_ptp_commands_in_hosts()
    # reboot_hosts()
    # ping_hosts()
    # download_linux_insert_pktgen_driver()
    # update_pi_scripts()

