import paramiko
import os

host_ip = {
    "dot10": "10.192.149.214",
    "dot20": "10.193.121.213",
    "dot30": "10.194.137.95",
    "dot40": "10.193.49.144",
    "dot50": "10.192.137.46",
    "dot60": "10.194.94.26"
}

local_data_location = "rhombus_data/"

flows = [
    {"id": "f1", "port": 10001, "client": "dot10", "server": "dot20", "rate": 0.33,
     "data_loc": "/home/pi/udp_server/", "user": "pi"},
    {"id": "f2", "port": 10002, "client": "dot30", "server": "dot20", "rate": 0.33,
     "data_loc": "/home/pi/udp_server/", "user": "pi"},
    {"id": "f3", "port": 10003, "client": "dot10", "server": "dot40", "rate": 0.33,
     "data_loc": "/home/pi/udp_server/", "user": "pi"},
    {"id": "f4", "port": 10004, "client": "dot10", "server": "dot40", "rate": 0.33,
     "data_loc": "/home/pi/udp_server/", "user": "pi"},
]


def run_cmd_via_paramiko(IP, port, username, password, command):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()
    s.connect(IP, port, username, password)
    (stdin, stdout, stderr) = s.exec_command(command)

    output = list(stdout.readlines())
    s.close()
    return output


def get_rhombus_data(file_suffix):
    for f in flows:
        remote_filepath = f["data_loc"] + f["id"] + file_suffix + ".csv"
        cmd = "scp " + f["user"] + "@" + host_ip[f["server"]] + ":" + remote_filepath + " " + local_data_location
        os.system(cmd)


def main():
    get_rhombus_data('_bg_diff_paths')
    #get_rhombus_data('_bg_same_paths')
    #get_rhombus_data('_no_bg_diff_paths')
    #get_rhombus_data('_no_bg_same_paths')

if __name__ == "__main__":
    main()
