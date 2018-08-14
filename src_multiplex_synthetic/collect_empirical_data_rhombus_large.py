import paramiko
import os
import numpy as np
import threading
import csv
import datetime
from collections import defaultdict
from flow_dict import all_flows as flows
#from flow_dict import flow_f1 as flows
#from flow_dict import flow_f2 as flows
#from flow_dict import flow_f3 as flows
#from flow_dict import flow_f4 as flows
#from flow_dict import flow_f5 as flows
#from flow_dict import flow_f6 as flows
#from flow_dict import flow_f7 as flows
#from flow_dict import flow_f8 as flows
from topo_dict import host_ip


client_process = "`echo $HOME`/Repositories/qos_synthesis/traffic_generation/udp_client/client"
server_process = "`echo $HOME`/Repositories/qos_synthesis/traffic_generation/udp_server/server"
should_nice = True


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


def client_command(server_ip, num_packets, flow_rate_in_Mbps, port_no):
    budget = (1E9 * 8) / (1024 * int(flow_rate_in_Mbps))

    client_command = ' '.join([client_process, server_ip, num_packets, str(int(budget)), str(port_no)])
    if should_nice == True:
        client_command = 'sudo nice --20 ' + client_command

    print client_command
    return client_command


def server_command(port_no, num_packets, flow_num, is_background, is_same):
    file_name = '_'.join([flow_num, is_background, is_same])
    output_file = '.'.join([file_name, 'csv'])
    server_command = ' '.join([server_process, port_no, num_packets]) + ' ' + output_file
    if should_nice == True:
        server_command = 'sudo nice --20 ' + server_command

    print server_command
    return server_command


def update_traffic_repo():
    for client in host_ip:
        print run_cmd_via_paramiko(host_ip[client][1], "cd Repositories/qos_synthesis; cd traffic_generation/;"
                                                       "cd udp_client/; make clean"
                                                       "cd ../udp_server/; make clean"
                                                       "cd ../../"
                                                       "git pull;")


def compile_traffic_repo():
    for client in host_ip:
        print run_cmd_via_paramiko(host_ip[client][1], "cd Repositories/qos_synthesis/traffic_generation/; "
                                                       "cd udp_server/; make; cd ../udp_client/; make;")


def clean_client_server():
    for client in host_ip:
        print run_cmd_via_paramiko(host_ip[client][1], "sudo pkill -x client; sudo pkill -x server; rm *.csv")

def update_pi_scripts():
    for client in host_ip:
        print run_cmd_via_paramiko(host_ip[client][1], "cd scripts/; rm -rf *; git init; git remote add origin "
                                                       "https://github.com/gopchandani/qos_synthesis.git; git pull;"
                                                       "git checkout pi_scripts ")

def start_all_flows_simultaneously(num_packets, is_background, is_same):
    server_thread_list = []
    client_thread_list = []

    for flow in flows:
        print
        print  host_ip[flow["client"]][0], '------->', host_ip[flow["server"]][0]
        server_thread = threading.Thread(target=run_cmd_via_paramiko, args=(host_ip[flow["server"]][1],
                                                                            server_command(str(flow['port']),
                                                                                           str(num_packets),
                                                                                           flow['id'], is_background,
                                                                                           is_same)))
        server_thread.start()
        server_thread_list.append(server_thread)

        client_thread = threading.Thread(target=run_cmd_via_paramiko, args=(host_ip[flow["client"]][1],
                                                                            client_command(host_ip[flow["server"]][0],
                                                                                           str(num_packets),
                                                                                           str(flow['rate']),
                                                                                           str(flow['port']))))
        client_thread.start()
        client_thread_list.append(client_thread)

    print 'Flows are running now'

    for client_thread in client_thread_list:
        client_thread.join()

    print 'Clients have finished sending the packets'

    for server_thread in server_thread_list:
        server_thread.join(10.0)

    print 'Servers have finished'

def main():

    # update_pi_scripts()
    clean_client_server()
    # update_traffic_repo()
    # compile_traffic_repo()

    num_packets = input('Enter the number of packets')
    background_traffic = input('Is there a background flow?')
    paths = input('Is it same or different paths?')

    is_background = 'bg' if background_traffic else 'nobg'
    is_same = 'same_paths' if paths else 'diff_paths'
    start_all_flows_simultaneously(num_packets, is_background, is_same)
    get_rhombus_data_pscp('_'.join([is_background, is_same]))

    #output_dir = get_rhombus_data_pscp('_'.join([is_background, is_same]))
    #processed_expt_output(os.getcwd() + "/" + output_dir)
    #processed_expt_output(os.getcwd() + "/" + "allflows_nobg")

    return 0


def get_rhombus_data(file_suffix):
    local_data_location = datetime.datetime.today().strftime('%Y-%m-%d')
    for f in flows:
        remote_filepath = f["data_loc"] + f["id"] + '_' + file_suffix + ".csv"
        cmd = "scp " + f["user"] + "@" + host_ip[f["server"]][1] + ":" + remote_filepath + " " + local_data_location
        os.system(cmd)


def get_rhombus_data_pscp(file_suffix):

    mydir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    os.makedirs(mydir)

    for f in flows:
        remote_filepath = f["data_loc"] + f["id"] + '_' + file_suffix + ".csv"

        cmd = "pscp " + "-pw raspberry " + f["user"] + "@" + host_ip[f["server"]][1] + ":" + remote_filepath + " " + mydir + '/'
        print cmd
        os.system(cmd)

    return mydir


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
            np.std(output[flow]),
            np.percentile(output[flow], 50),
            np.percentile(output[flow], 99),
            np.percentile(output[flow], 99.9)
        ))


if __name__ == "__main__":
    main()
