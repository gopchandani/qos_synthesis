import paramiko
import os
import threading
import datetime

host_ip = {
    "dot08": ["192.168.1.8", "10.192.180.112"],
    "dot09": ["192.168.1.9", "10.193.188.190"],
    "dot10": ["192.168.1.10", "10.193.198.88"],
    "dot11": ["192.168.1.11", "10.192.92.86"],
    "dot12": ["192.168.1.12", "10.193.57.162"],
    "dot15": ["192.168.1.15", "10.195.168.155"],
    "dot20": ["192.168.1.20", "10.194.58.113"],
    "dot29": ["192.168.1.29", "10.192.189.214"],
    "dot30": ["192.168.1.30", "10.195.27.95"],
    "dot31": ["192.168.1.31", "10.193.242.20"],
    "dot40": ["192.168.1.40", "10.193.31.152"]
}

client_process = "`echo $HOME`/Repositories/qos_synthesis/traffic_generation/udp_client/client"
server_process = "`echo $HOME`/Repositories/qos_synthesis/traffic_generation/udp_server/server"


should_nice = False

flows = [
    {"id": "f1", "port": 10000, "client": "dot08", "server": "dot40", "rate": 20,
     "data_loc": "/home/pi/", "user": "pi"},
    {"id": "f2", "port": 10001, "client": "dot10", "server": "dot40", "rate": 20,
     "data_loc": "/home/pi/", "user": "pi"},
    {"id": "f3", "port": 10002, "client": "dot12", "server": "dot40", "rate": 20,
     "data_loc": "/home/pi/", "user": "pi"},
    {"id": "f4", "port": 10003, "client": "dot09", "server": "dot20", "rate": 20,
     "data_loc": "/home/iti/", "user": "iti"},
    {"id": "f5", "port": 10004, "client": "dot10", "server": "dot20", "rate": 20,
     "data_loc": "/home/iti/", "user": "iti"},
    {"id": "f6", "port": 10005, "client": "dot11", "server": "dot20", "rate": 20,
     "data_loc": "/home/iti/", "user": "iti"},
    {"id": "f7", "port": 10006, "client": "dot29", "server": "dot20", "rate": 20,
     "data_loc": "/home/iti/", "user": "iti"},
    {"id": "f8", "port": 10007, "client": "dot30", "server": "dot20", "rate": 20,
     "data_loc": "/home/iti/", "user": "iti"},
    {"id": "f9", "port": 10008, "client": "dot31", "server": "dot20", "rate": 20,
     "data_loc": "/home/iti/", "user": "iti"},
    {"id": "f10", "port": 10009, "client": "dot15", "server": "dot40", "rate": 20,
     "data_loc": "/home/pi/", "user": "pi"},
    {"id": "f11", "port": 10010, "client": "dot15", "server": "dot40", "rate": 20,
     "data_loc": "/home/pi/", "user": "pi"}
]


def run_cmd_via_paramiko(IP, command, port=22, username='pi', password='raspberry'):

    if IP == host_ip['dot20'][1]:
        username = 'iti'
        password = 'csl440'

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
    #server_command = ' '.join([server_process, port_no, num_packets]) + ' > ' + output_file
    server_command = ' '.join([server_process, port_no, num_packets]) + ' ' + output_file
    if should_nice == True:
        server_command = 'sudo nice --20 ' + server_command

    print server_command
    return server_command


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
        server_thread.join(5.0)

    print 'Servers have finished'

def main():

    num_packets = input('Enter the number of packets')
    background_traffic = input('Is there a background flow?')
    paths = input('Is it same or different paths?')

    for client in host_ip:
        print run_cmd_via_paramiko(host_ip[client][1], "sudo pkill -x client; sudo pkill -x server")
        #print run_cmd_via_paramiko(host_ip[client][1], "cd Repositories/qos_synthesis/traffic_generation/udp_server; make clean; make;")
        #print run_cmd_via_paramiko(host_ip[client][1], "cd Repositories/qos_synthesis/traffic_generation/udp_client; make clean; make;")

    is_background = 'bg' if background_traffic else 'nobg'
    is_same = 'same_paths' if paths else 'diff_paths'
    start_all_flows_simultaneously(num_packets, is_background, is_same)

    get_rhombus_data_pscp('_'.join([is_background, is_same]))
    return


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
        if host_ip[f["server"]][0] == host_ip["dot40"][0]:
            cmd = "pscp " + "-pw raspberry " + f["user"] + "@" + host_ip[f["server"]][1] + ":" + remote_filepath + " " + mydir + '/'
        else:
            cmd = "pscp " + "-pw csl440 " + f["user"] + "@" + host_ip[f["server"]][1] + ":" + remote_filepath + " " + mydir + '/'
        print cmd

        os.system(cmd)

if __name__ == "__main__":
    main()
