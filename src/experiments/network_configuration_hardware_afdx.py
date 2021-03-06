__author__ = 'Rakesh Kumar'

import os, json
import networkx as nx
import paramiko
paramiko.util.log_to_file("filename.log")


class NetworkConfigurationHardwareNsdi(object):

    def __init__(self):
       self.graph = nx.DiGraph()

    def run_cmd_via_paramiko(self, IP, port, username, password, command):

        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.load_system_host_keys()
        s.connect(IP, port, username, password)
        (stdin, stdout, stderr) = s.exec_command(command)

        output = list(stdout.readlines())
        s.close()
        return output


    def clear_all_flows_queues(self):

        for switch_dict in self.switch_dict_iter():

            delete_flows_cmd = 'ovs-ofctl del-flows ' + 'tcp:' + str(switch_dict["switch_ip"]) + ':' +  \
                               str(switch_dict["of_port"])



            os.system(delete_flows_cmd)

            # print("delete_flows_cmd done")

            delete_groups_cmd = 'ovs-ofctl -O OpenFlow13 del-groups ' + 'tcp:' + str(switch_dict["switch_ip"]) + ':' + \
                                str(switch_dict["of_port"])

            os.system(delete_groups_cmd)

            # print("delete_groups_cmd done")


            for port in switch_dict["port_list"]:

                port_clear_qos_cmd = "ovs-vsctl " + "--db=tcp:" + str(switch_dict["switch_ip"]) + ":6634 -- " + \
                                     "clear Port " + port + " qos"
                os.system(port_clear_qos_cmd)
                print(port_clear_qos_cmd)

            print("port_clear_qos_cmd done")


            destroy_qos_cmd = "ovs-vsctl " + "--db=tcp:" + str(switch_dict["switch_ip"]) + ":6634 -- " + \
                              "--all destroy qos"

            os.system(destroy_qos_cmd)

            print("destroy_qos_cmd done")

            destroy_queue_cmd = "ovs-vsctl " + "--db=tcp:" + str(switch_dict["switch_ip"]) + ":6634 -- " + \
                                "--all destroy queue"

            os.system(destroy_queue_cmd)

            print("destroy_queue_cmd done")

    def add_switches(self):
        switch_dict= {"switch_name": "ps1",
                      "bridge_name": "br0",
                      "switch_ip": "192.17.101.126",
                      "usr": "admin",
                      "psswd": "csl440",
                      "of_port": "6633",
                      "port_list":['ge-1/1/1','ge-1/1/2', 'ge-1/1/3', 'ge-1/1/4'],
                      "egress_port_list": ['ge-1/1/2', 'ge-1/1/4']
                      }

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)

        switch_dict = {"switch_name": "ps2",
                       "bridge_name": "br0",
                       "switch_ip": "192.17.101.127",
                       "usr": "admin",
                       "psswd": "csl440",
                       "of_port": "6633",
                       "port_list":['ge-1/1/1', 'ge-1/1/3', 'ge-1/1/5', 'ge-1/1/7', 'ge-1/1/9',
                                    'ge-1/1/2', 'ge-1/1/4', 'ge-1/1/6'],
                       "egress_port_list": ['ge-1/1/2','ge-1/1/4', 'ge-1/1/6']
                       }

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)

        switch_dict = {"switch_name": "ps3",
                       "bridge_name": "br0",
                       "switch_ip": "192.17.101.128",
                       "usr": "admin",
                       "psswd": "csl440",
                       "of_port": "6633",
                       "port_list": ['ge-1/1/1', 'ge-1/1/3', 'ge-1/1/5', 'ge-1/1/7', 'ge-1/1/9',
                                     'ge-1/1/4', 'ge-1/1/8', 'ge-1/1/10'],
                       "egress_port_list": ['ge-1/1/4', 'ge-1/1/8', 'ge-1/1/10']
                       }

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)

        switch_dict = {"switch_name": "ps4",
                       "bridge_name": "br0",
                       "switch_ip": "192.17.101.129",
                       "usr": "admin",
                       "psswd": "csl440",
                       "of_port": "6633",
                       "port_list": ['ge-1/1/1', 'ge-1/1/3', 'ge-1/1/5', 'ge-1/1/7', 'ge-1/1/9', 'ge-1/1/11',
                                    'ge-1/1/2', 'ge-1/1/4'],
                       "egress_port_list": ['ge-1/1/1', 'ge-1/1/3', 'ge-1/1/5', 'ge-1/1/7', 'ge-1/1/9', 'ge-1/1/11']
                       }

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)


    def is_switch(self, node_id):
        if self.graph.node[node_id]["node_type"] == "switch":
            return True
        else:
            return False

    def is_host(self, node_id):
        if self.graph.node[node_id]["node_type"] == "host":
            return True
        else:
            return False



    def get_host_dict(self, host_id):
        return self.graph.node[host_id]['h']

    def get_switch_dict(self, switch_id):
        return self.graph.node[switch_id]['b']

    def get_link_dict(self, node1_id, node2_id):
        return self.graph[node1_id][node2_id]['l']

    def add_host_nodes(self):

        hosts = [
            # Switch 1
            ("dot31", "ps1", "192.168.1.31", "10.194.136.140", "pi", "raspberry"),
            ("dot120", "ps1", "192.168.1.120", "10.195.185.109", "pi", "raspberry"),

            # Switch 2
            ("dot08", "ps2", "192.168.1.8", "10.193.128.19", "pi", "raspberry"),
            ("dot10", "ps2", "192.168.1.10", "10.194.217.111", "pi", "raspberry"),
            ("dot12", "ps2", "192.168.1.12", "10.193.57.162", "pi", "raspberry"),
            ("dot30", "ps2", "192.168.1.30", "10.192.240.91", "pi", "raspberry"),
            ("dot140", "ps2", "192.168.1.140", "10.194.183.169", "pi", "raspberry"),

            # Switch 3
            ("dot15", "ps3", "192.168.1.15", "10.195.12.184", "pi", "raspberry"),
            ("dot20", "ps3", "192.168.1.20", "10.193.9.207", "pi", "raspberry"),
            ("dot200", "ps3", "192.168.1.200", "10.192.244.103", "pi", "raspberry"),
            ("dot220", "ps3", "192.168.1.220", "10.195.83.193", "pi", "raspberry"),
            ## Background
            ("dot250", "ps3", "192.168.1.250", "10.194.228.155", "iti", "csl440"),

            # Switch 4
            ("dot09", "ps4", "192.168.1.09", "10.194.111.180", "pi", "raspberry"),
            ("dot11", "ps4", "192.168.1.11", "10.194.17.214", "pi", "raspberry"),
            #("dot29", "ps4", "192.168.1.29", "10.194.188.181", "pi", "raspberry"),
            ("dot244", "ps4", "192.168.1.244", "10.195.78.41", "pi", "raspberry"),
            ("dot40", "ps4", "192.168.1.40", "10.194.159.20", "pi", "raspberry"),
            #("dot240", "ps4", "192.168.1.240", "10.193.140.82", "pi", "raspberry"),
            ("dot248", "ps4", "192.168.1.248", "10.193.109.118", "pi", "raspberry"),
            ## Background
            ("dot123", "ps4", "192.168.1.123", "10.194.45.147", "iti", "csl440"),
        ]

        self.add_hosts(hosts)

    def add_hosts(self, hosts):
        for host_name, switch_id, host_ip, mgmt_ip, usr, psswd in hosts:
            host_dict = {
                "host_name": host_name,
                "switch_id": switch_id,
                "host_ip": host_ip,
                "mgmt_ip": mgmt_ip,
                "usr": usr,
                "psswd": psswd
            }

            self.graph.add_node(host_dict["host_name"],
                                node_type="host",
                                h=host_dict)

    def switch_attached_host_dicts(self,switch_dict):
        host_dict_list=[]

        for host_dict in self.host_dict_iter():
                if host_dict["switch_id"] == switch_dict["switch_name"]:
                    host_dict_list.append(host_dict)

        return host_dict_list

    def host_dict_iter(self):
        for node_id in self.graph.node():

            if self.graph.node[node_id]['node_type'] == "host":
                yield self.graph.node[node_id]['h']

    def switch_dict_iter(self):
        for node_id in self.graph.node():

            if self.graph.node[node_id]['node_type'] == "switch":
                yield self.graph.node[node_id]['b']

    def get_node_type(self, node_id):
        node_type = None

        if self.graph.has_node(node_id):
            node_type = self.graph.node[node_id]["node_type"]

        return node_type

    def add_host_links(self):

        pi_to_switch_bw = 1000000 * 50 #Assume pi to switch bandwidth is 50 Mbps
        pi_to_switch_delay = 10e-6 * 10 # Assumes pi to switch latency is 10 microseconds

        laptop_to_switch_bw = 10000000 * 50
        laptop_to_switch_delay = 10e-6 * 10 # Assumes pi to switch latency is 10 microseconds


        links = [
                 # Switch 1
                 ("dot31", "ps1", "eth0", "ge-1/1/1", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot120", "ps1", "eth0", "ge-1/1/3", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 # Switch 2
                 ("dot08", "ps2", "eth0", "ge-1/1/1", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot10", "ps2", "eth0", "ge-1/1/3", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot12", "ps2", "eth0", "ge-1/1/5", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot30", "ps2", "eth0", "ge-1/1/7", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot140", "ps2", "eth0", "ge-1/1/9", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 # Switch 3
                 ("dot15", "ps3", "eth0", "ge-1/1/1", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot20", "ps3", "eth0", "ge-1/1/3", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot200", "ps3", "eth0", "ge-1/1/5", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot220", "ps3", "eth0", "ge-1/1/7", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot250", "ps3", "enp0s25", "ge-1/1/9", "host-sw", laptop_to_switch_bw, laptop_to_switch_delay),

                 # Switch 4
                 ("dot09", "ps4", "eth0", "ge-1/1/1", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot11", "ps4", "eth0", "ge-1/1/3", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot244", "ps4", "eth0", "ge-1/1/5", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 #("dot29", "ps4", "eth0", "ge-1/1/5", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot40", "ps4", "eth0", "ge-1/1/7", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 #("dot240", "ps4", "eth0", "ge-1/1/9", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot248", "ps4", "eth0", "ge-1/1/9", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
                 ("dot123", "ps4", "enp0s31f6", "ge-1/1/11", "host-sw", laptop_to_switch_bw, laptop_to_switch_delay)
        ]

        self.add_links(links)


    def add_links(self, links):
        for node1, node2, node1_port, node2_port, link_type, bw, delay in links:
            link_dict = {
                "node1": node1,
                "node2": node2,
                "node1_port": node1_port,
                "node2_port": node2_port,
                "bw": bw,
                "delay":delay
            }

            self.graph.add_edge(link_dict["node1"],
                                link_dict["node2"],
                                l=link_dict, t=link_type)
            link_dict = {
                "node1": node2,
                "node2": node1,
                "node1_port": node2_port,
                "node2_port": node1_port,
                "bw": bw,
                "delay": delay
            }

            self.graph.add_edge(link_dict["node1"],
                                link_dict["node2"],
                                l=link_dict, t=link_type)

    def add_switch_links(self):

        switch_to_switch_bw = 1000000 * 1000 * 10  # Assume pi to switch bandwidth is 10 Gbps
        switch_to_switch_delay = 10e-9 * 10  # Assumes pi to switch latency is 10 nanoseconds

        links = [
                ("ps1", "ps2", "ge-1/1/2", "ge-1/1/2","sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                ("ps1", "ps3", "ge-1/1/4", "ge-1/1/4", "sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                ("ps2", "ps3", "ge-1/1/4", "ge-1/1/8","sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                ("ps2", "ps4", "ge-1/1/6", "ge-1/1/2", "sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                ("ps3", "ps4", "ge-1/1/10", "ge-1/1/4","sw-sw", switch_to_switch_bw, switch_to_switch_delay)
        ]

        self.add_links(links)


    def setup_network_configuration(self):

        # These things are needed by network graph...

        self.add_host_nodes()
        # print("add host nodes done")
        self.add_switches()
        # print("add switches done")
        self.add_host_links()
        # print("add host links done")
        self.add_switch_links()
        # print("add switch links done")
        # self.clear_all_flows_queues()
        # print("clear all flows done")


