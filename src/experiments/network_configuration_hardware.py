__author__ = 'Rakesh Kumar'

import httplib2
import os

from socket import *
import networkx as nx

import paramiko
paramiko.util.log_to_file("filename.log")


class NetworkConfigurationHardware(object):

    def __init__(self, controller,
                 conf_root,
                 flow_specs):

        self.controller = controller
        self.conf_root = conf_root
        self.flow_specs = flow_specs

        self.graph = nx.DiGraph()

        self.controller_port = 6666
        self.nc_topo_str = None

        self.conf_path = self.conf_root + str(self) + "/"
        if not os.path.exists(self.conf_path):
            os.makedirs(self.conf_path)
            self.load_config = False
            self.save_config = True
        else:
            self.load_config = True
            self.save_config = False

        # Initialize things to talk to controller
        self.baseUrlRyu = "http://192.168.1.102:8080/"

        self.h = httplib2.Http(".cache")
        self.h.add_credentials('admin', 'admin')

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

        for bridge_dict in self.bridge_dict_iter():

            self.run_cmd_via_paramiko(bridge_dict["switch_IP"],
                                      22,
                                      bridge_dict["usr"],
                                      bridge_dict["psswd"],
                                      "/ovs/bin/ovs-ofctl del-flows " +  bridge_dict["bridge_name"])

            self.run_cmd_via_paramiko(bridge_dict["switch_IP"],
                                      22,
                                      bridge_dict["usr"],
                                      bridge_dict["psswd"],
                                      "/ovs/bin/ovs-vsctl --all destroy qos")

            self.run_cmd_via_paramiko(bridge_dict["switch_IP"],
                                      22,
                                      bridge_dict["usr"],
                                      bridge_dict["psswd"],
                                      "/ovs/bin/ovs-vsctl --all destroy queue")

            for port in bridge_dict["port_list"]:
                self.run_cmd_via_paramiko(bridge_dict["switch_IP"],
                                          22,
                                          bridge_dict["usr"],
                                          bridge_dict["psswd"],
                                          "/ovs/bin/ovs-vsctl clear Port " + port + " qos")

    def add_bridges(self):
        bridge_dict= {"bridge_name": "br0",
                      "switch_IP": "192.168.1.101",
                      "usr": "admin",
                      "psswd": "password",
                      "of_port": "1235",
                      "port_list":['ge-1/1/25','ge-1/1/27','ge-1/1/29']}

        self.graph.add_node(bridge_dict["bridge_name"], node_type="bridge", b=bridge_dict)

        bridge_dict = {"bridge_name": "br1",
                       "switch_IP": "192.168.1.101",
                       "usr": "admin",
                       "psswd": "password",
                       "of_port": "1236",
                       "port_list":['ge-1/1/31', 'ge-1/1/33', 'ge-1/1/35']}

        self.graph.add_node(bridge_dict["bridge_name"], node_type="bridge", b=bridge_dict)

        bridge_dict = {"bridge_name": "br2",
                       "switch_IP": "192.168.1.101",
                       "usr": "admin",
                       "psswd": "password",
                       "of_port": "1237",
                       "port_list":['ge-1/1/37', 'ge-1/1/39', 'ge-1/1/41']}

        self.graph.add_node(bridge_dict["bridge_name"], node_type="bridge", b=bridge_dict)

        bridge_dict = {"bridge_name": "of-switch",
                       "switch_IP": "192.168.1.101",
                       "usr": "admin",
                       "psswd": "password",
                       "of_port": "1234",
                       "port_list": ['ge-1/1/43', 'ge-1/1/45', 'ge-1/1/47']}

        self.graph.add_node(bridge_dict["bridge_name"], node_type="bridge", b=bridge_dict)

    def get_host_dict(self, host_id):
        return self.graph.node[host_id]['h']

    def get_bridge_dict(self, bridge_id):
        return self.graph.node[bridge_id]['b']

    def get_link_dict(self, node1_id, node2_id):
        return self.graph[node1_id][node2_id]['l']

    def add_host_nodes(self):

        host_dict = {"host_name": "e5",
                     "bridge_id" : "br0",
                     "host_IP": "192.168.1.10",
                     "mgmt_ip": "10.192.149.214",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:7a:19:e5"}

        self.graph.add_node(host_dict["host_name"], node_type="host", h=host_dict)

        host_dict = {"host_name": "7e",
                     "bridge_id": "br2",
                     "host_IP": "192.168.1.20",
                     "mgmt_ip": "10.194.179.16",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:8b:02:7e"}

        self.graph.add_node(host_dict["host_name"], node_type="host", h=host_dict)

        host_dict = {"host_name": "66",
                     "bridge_id": "of-switch",
                     "host_IP": "192.168.1.30",
                     "mgmt_ip": "10.195.162.179",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:4b:c7:66"}

        self.graph.add_node(host_dict["host_name"], node_type="host", h=host_dict)

        host_dict = {"host_name": "38",
                     "bridge_id": "br1",
                     "host_IP": "192.168.1.40",
                     "mgmt_ip": "10.193.214.117",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:6b:f7:38"}

        self.graph.add_node(host_dict["host_name"], node_type="host", h=host_dict)

    def bridge_attached_host_dicts(self,bridge_dict):
        host_dict_list=[]

        for host_dict in self.host_dict_iter():
                if host_dict["bridge_id"] == bridge_dict["bridge_name"]:
                    host_dict_list.append(host_dict)

        return host_dict_list

    def host_dict_iter(self):
        for node_id in self.graph.node():

            if self.graph.node[node_id]['node_type'] == "host":
                yield self.graph.node[node_id]['h']

    def bridge_dict_iter(self):
        for node_id in self.graph.node():

            if self.graph.node[node_id]['node_type'] == "bridge":
                yield self.graph.node[node_id]['b']

    def get_node_type(self, node_id):
        node_type = None

        if self.graph.has_node(node_id):
            node_type = self.graph.node[node_id]["node_type"]

        return node_type

    def add_host_links(self):

        pi_to_switch_bw = 1000000 * 50 #Assume pi to switch bandwidth is 50 Mbps
        pi_to_switch_delay = 10e-6 * 10 # Assumes pi to switch latency is 10 microseconds
        link_dict = {"node1" : "38",
                     "node1_port" : "eth0",
                     "node2" : "br1",
                     "node2_port" : "ge-1/1/31",
                     "bw" : pi_to_switch_bw,
                     "delay" :pi_to_switch_delay}

        self.graph.add_edge(link_dict["node1"],
                            link_dict["node2"],
                            l=link_dict)

        link_dict = {"node1" : "66",
                     "node1_port" : "eth0",
                     "node2" : "of-switch",
                     "node2_port" : "ge-1/1/43",
                     "bw" : pi_to_switch_bw,
                     "delay" :pi_to_switch_delay}

        self.graph.add_edge(link_dict["node1"],
                            link_dict["node2"],
                            l=link_dict)

        link_dict = {"node1" : "7e",
                     "node1_port" : "eth0",
                     "node2" : "br2",
                     "node2_port" : "ge-1/1/37",
                     "bw" : pi_to_switch_bw,
                     "delay" :pi_to_switch_delay}

        self.graph.add_edge(link_dict["node1"],
                            link_dict["node2"],
                            l=link_dict)

        link_dict = {"node1" : "e5",
                     "node1_port" : "eth0",
                     "node2" : "br0",
                     "node2_port" : "ge-1/1/25",
                     "bw" : pi_to_switch_bw,
                     "delay" :pi_to_switch_delay}

        self.graph.add_edge(link_dict["node1"],
                            link_dict["node2"],
                            l=link_dict)

        link_dict = {"node2": "38",
                     "node2_port": "eth0",
                     "node1": "br1",
                     "node1_port": "ge-1/1/31",
                     "bw": pi_to_switch_bw,
                     "delay": pi_to_switch_delay}

        self.graph.add_edge(link_dict["node1"],
                            link_dict["node2"],
                            l=link_dict)

        link_dict = {"node2": "66",
                     "node2_port": "eth0",
                     "node1": "of-switch",
                     "node1_port": "ge-1/1/43",
                     "bw": pi_to_switch_bw,
                     "delay": pi_to_switch_delay}

        self.graph.add_edge(link_dict["node1"],
                            link_dict["node2"],
                            l=link_dict)

        link_dict = {"node2": "7e",
                     "node2_port": "eth0",
                     "node1": "br2",
                     "node1_port": "ge-1/1/37",
                     "bw": pi_to_switch_bw,
                     "delay": pi_to_switch_delay}

        self.graph.add_edge(link_dict["node1"],
                            link_dict["node2"],
                            l=link_dict)

        link_dict = {"node2": "e5",
                     "node2_port": "eth0",
                     "node1": "br0",
                     "node1_port": "ge-1/1/25",
                     "bw": pi_to_switch_bw,
                     "delay": pi_to_switch_delay}

        self.graph.add_edge(link_dict["node1"],
                            link_dict["node2"],
                            l=link_dict)

    def add_bridge_links(self):

        bridge_to_bridge_bw = 1000000 * 1000 * 10  # Assume pi to switch bandwidth is 10 Gbps
        bridge_to_bridge_delay = 10e-9 * 10  # Assumes pi to switch latency is 10 nanoseconds

        links = [("br0", "of-switch", "ge-1/1/29", "ge-1/1/45"),
                 ("br0", "br2", "ge-1/1/27", "ge-1/1/39"),
                 ("of-switch", "br1", "ge-1/1/47", "ge-1/1/35"),
                 ("br1", "br2", "ge-1/1/33", "ge-1/1/41")]

        for node1, node2, node1_port, node2_port in links:
            link_dict = {
                "node1": node1,
                "node2": node2,
                "node1_port": node1_port,
                "node2_port": node2_port,
                "bw": bridge_to_bridge_bw,
                "delay":bridge_to_bridge_delay
            }

            self.graph.add_edge(link_dict["node1"],
                                link_dict["node2"],
                                l=link_dict)
            link_dict = {
                "node1": node2,
                "node2": node1,
                "node1_port": node2_port,
                "node2_port": node1_port,
                "bw": bridge_to_bridge_bw,
                "delay": bridge_to_bridge_delay
            }

            self.graph.add_edge(link_dict["node1"],
                                link_dict["node2"],
                                l=link_dict)


    def setup_network_configuration(self):

        # These things are needed by network graph...
        self.add_host_nodes()
        self.add_bridges()
        self.add_host_links()
        self.add_bridge_links()


