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

            delete_flows_cmd = 'ovs-ofctl del-flows ' + 'tcp:' + str(switch_dict["switch_ip"]) + ':' + \
                            str(switch_dict["of_port"])
            print(delete_flows_cmd)

            os.system(delete_flows_cmd)

            delete_groups_cmd = 'ovs-ofctl -O OpenFlow13 del-groups ' + 'tcp:' + str(switch_dict["switch_ip"]) + ':' + \
                            str(switch_dict["of_port"])
            print(delete_groups_cmd)

            os.system(delete_groups_cmd)


            for port in switch_dict["port_list"]:

                port_clear_qos_cmd = "ovs-vsctl " + "--db=tcp:" + str(switch_dict["switch_ip"]) + ":6634 -- " + \
                            "clear Port " + port + " qos"
                print(port_clear_qos_cmd)
                os.system(port_clear_qos_cmd)


            destroy_qos_cmd = "ovs-vsctl " + "--db=tcp:" + str(switch_dict["switch_ip"]) + ":6634 -- " + \
                            "--all destroy qos"

            print(destroy_qos_cmd)
            os.system(destroy_qos_cmd)

            destroy_queue_cmd = "ovs-vsctl " + "--db=tcp:" + str(switch_dict["switch_ip"]) + ":6634 -- " + \
                            "--all destroy queue"
            print(destroy_queue_cmd)
            os.system(destroy_queue_cmd)

        print("---- Clear all flows queues done")

    def add_switches(self):
        switch_dict= {"switch_name": "ps1",
                      "bridge_name": "br0",
                      "switch_ip": "192.17.101.126",
                      "usr": "admin",
                      "psswd": "csl440",
                      "of_port": "6633",
                      "port_list":['ge-1/1/1', 'ge-1/1/46', 'ge-1/1/47', 'ge-1/1/48']
                      }

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)

        switch_dict = {"switch_name": "ps2",
                       "bridge_name": "br0",
                       "switch_ip": "192.17.101.127",
                       "usr": "admin",
                       "psswd": "csl440",
                       "of_port": "6633",
                       "port_list":['ge-1/1/46', 'ge-1/1/47', 'ge-1/1/48']
                       }

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)

        switch_dict = {"switch_name": "ps3",
                       "bridge_name": "br0",
                       "switch_ip": "192.17.101.128",
                       "usr": "admin",
                       "psswd": "csl440",
                       "of_port": "6633",
                       "port_list": ['ge-1/1/1', 'ge-1/1/3', 'ge-1/1/5', 'ge-1/1/7', 'ge-1/1/9', 'ge-1/1/11',
                                     'ge-1/1/13', 'ge-1/1/15', 'ge-1/1/17', 'ge-1/1/19', 'ge-1/1/21', 'ge-1/1/23',
                                     'ge-1/1/25', 'ge-1/1/46','ge-1/1/47', 'ge-1/1/48']
                       }

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)

        switch_dict = {"switch_name": "ps4",
                       "bridge_name": "br0",
                       "switch_ip": "192.17.101.129",
                       "usr": "admin",
                       "psswd": "csl440",
                       "of_port": "6633",
                       "port_list": ['ge-1/1/2', 'ge-1/1/4', 'ge-1/1/6', 'ge-1/1/8', 'ge-1/1/10', 'ge-1/1/12',
                                     'ge-1/1/14', 'ge-1/1/16', 'ge-1/1/18', 'ge-1/1/20', 'ge-1/1/22', 'ge-1/1/24',
                                     'ge-1/1/26', 'ge-1/1/28', 'ge-1/1/46', 'ge-1/1/47', 'ge-1/1/48']
                       }

        self.graph.add_node(switch_dict["switch_name"], node_type="switch", b=switch_dict)
        print("---- Adding of switches done")

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
            # ("dot08", "ps3", "192.168.1.8", "10.194.195.16", "pi", "raspberry"),
            # ("dot10", "ps3", "192.168.1.10", "10.193.145.133", "pi", "raspberry"),
            # ("dot12", "ps3", "192.168.1.12", "10.193.57.162", "pi", "raspberry"),
            # ("dot20", "ps3", "192.168.1.20", "10.195.240.61", "pi", "raspberry"),
            # ("dot30", "ps3", "192.168.1.30", "10.192.240.91", "pi", "raspberry"),
            # ("dot40", "ps3", "192.168.1.40", "10.194.159.20", "pi", "raspberry"),
            # ("dot50", "ps3", "192.168.1.50", "10.192.181.58", "pi", "raspberry"),
            # ("dot70", "ps3", "192.168.1.70", "10.195.145.47", "pi", "raspberry"),
            # ("dot140", "ps3", "192.168.1.140", "10.194.183.169", "pi", "raspberry"),
            # ("dot220", "ps3", "192.168.1.220", "10.192.1.44", "pi", "raspberry"),
            # ("dot242", "ps3", "192.168.1.242", "10.192.159.135", "pi", "raspberry"),
            # ("dot245", "ps3", "192.168.1.245", "10.195.108.69", "pi", "raspberry"),
            # ("dot247", "ps3", "192.168.1.247", "10.193.221.100", "pi", "raspberry"),
            # ("dot250", "ps1", "192.168.1.250", "10.194.228.155", "iti", "csl440"),
            #
            # ("dot09", "ps4", "192.168.1.9", "10.194.111.180", "pi", "raspberry"),
            # ("dot11", "ps4", "192.168.1.11", "10.194.217.111", "pi", "raspberry"),
            # ("dot15", "ps4", "192.168.1.15", "10.195.12.184", "pi", "raspberry"),
            # ("dot29", "ps4", "192.168.1.29", "10.195.182.146", "pi", "raspberry"),
            # ("dot31", "ps4", "192.168.1.31", "10.195.67.42", "pi", "raspberry"),
            # ("dot120", "ps4", "192.168.1.120", "10.193.249.20", "pi", "raspberry"),
            # ("dot60", "ps4", "192.168.1.60", "10.194.255.221", "pi", "raspberry"),
            # ("dot80", "ps4", "192.168.1.80", "10.193.186.173", "pi", "raspberry"),
            # ("dot200", "ps4", "192.168.1.200", "10.192.243.200", "pi", "raspberry"),
            # ("dot240", "ps4", "192.168.1.240", "10.193.140.82", "pi", "raspberry"),
            # ("dot244", "ps4", "192.168.1.244", "10.195.78.41", "pi", "raspberry"),
            # ("dot246", "ps4", "192.168.1.246", "10.194.17.162", "pi", "raspberry"),
            # ("dot248", "ps4", "192.168.1.248", "10.193.109.118", "pi", "raspberry"),
            # ("dot123", "ps4", "192.168.1.123", "10.195.45.147", "iti", "csl440"),

            # ("dot102", "ps1", "192.168.1.102", "10.194.94.27", "sdn", "sdnqos"),

            ## For Per packet Processing delay
            ##################################
            ("dot08", "ps1", "192.168.1.8", "10.194.195.16", "pi", "raspberry"),
            ("dot09", "ps1", "192.168.1.9", "10.194.111.180", "pi", "raspberry"),
            ##################################

        ]

        self.add_hosts(hosts)
        print("---- Adding of hosts done")


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
            #      ("dot08", "ps3", "eth0", "ge-1/1/1", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot10", "ps3", "eth0", "ge-1/1/3", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot12", "ps3", "eth0", "ge-1/1/5", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot20", "ps3", "eth0", "ge-1/1/7", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot30", "ps3", "eth0", "ge-1/1/9", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot40", "ps3", "eth0", "ge-1/1/11", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot50", "ps3", "eth0", "ge-1/1/13", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot70", "ps3", "eth0", "ge-1/1/15", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot140", "ps3", "eth0", "ge-1/1/17", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot220", "ps3", "eth0", "ge-1/1/19", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot242", "ps3", "eth0", "ge-1/1/21", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot245", "ps3", "eth0", "ge-1/1/23", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot247", "ps3", "eth0", "ge-1/1/25", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot250", "ps1", "enp0s25", "ge-1/1/1", "host-sw", laptop_to_switch_bw, laptop_to_switch_delay),
            #
            #      ("dot09", "ps4", "eth0", "ge-1/1/2", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot11", "ps4", "eth0", "ge-1/1/4", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot15", "ps4", "eth0", "ge-1/1/6", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot29", "ps4", "eth0", "ge-1/1/8", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot31", "ps4", "eth0", "ge-1/1/10", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot120", "ps4", "eth0", "ge-1/1/12", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot60", "ps4", "eth0", "ge-1/1/14", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot80", "ps4", "eth0", "ge-1/1/16", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot200", "ps4", "eth0", "ge-1/1/18", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot240", "ps4", "eth0", "ge-1/1/20", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot244", "ps4", "eth0", "ge-1/1/22", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot246", "ps4", "eth0", "ge-1/1/24", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot248", "ps4", "eth0", "ge-1/1/26", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            #      ("dot123", "ps4", "enp0s31f6", "ge-1/1/28", "host-sw", laptop_to_switch_bw, laptop_to_switch_delay),

            ## For Per packet Processing delay
            ##################################
            ("dot08", "ps1", "eth0", "ge-1/1/46", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            ("dot09", "ps1", "eth0", "ge-1/1/48", "host-sw", pi_to_switch_bw, pi_to_switch_delay),
            ##################################

        ]

        self.add_links(links)
        print("---- Adding of host links done")


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

                 # ("ps1", "ps2", "ge-1/1/46", "ge-1/1/46","sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                 # ("ps1", "ps3", "ge-1/1/48", "ge-1/1/48", "sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                 # ("ps2", "ps3", "ge-1/1/47", "ge-1/1/47","sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                 # ("ps2", "ps4", "ge-1/1/48", "ge-1/1/48", "sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                 # ("ps3", "ps4", "ge-1/1/46", "ge-1/1/46","sw-sw", switch_to_switch_bw, switch_to_switch_delay)

                ## For Per packet Processing delay
                ##################################
                # ("ps1", "ps2", "ge-1/1/48", "ge-1/1/47", "sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                # ("ps2", "ps3", "ge-1/1/48", "ge-1/1/47", "sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                # ("ps3", "ps4", "ge-1/1/48", "ge-1/1/46", "sw-sw", switch_to_switch_bw, switch_to_switch_delay),
                ##################################

                ## For Per packet Processing delay 1 switch
                ##################################
                #### No switch-switch links
                ##################################
         ]
        self.add_links(links)
        print("---- Adding of switch links done")


    def setup_network_configuration(self):

        # These things are needed by network graph...
        self.add_host_nodes()
        self.add_switches()
        self.add_host_links()
        self.add_switch_links()
        # self.clear_all_flows_queues()


