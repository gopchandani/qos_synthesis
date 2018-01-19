__author__ = 'Rakesh Kumar'

import httplib2
import os

from socket import *
import networkx as nx




class NetworkConfigurationHardware\

            (object):

    def __init__(self, controller,
                 conf_root,
                 flow_specs):

        self.controller = controller
        self.conf_root = conf_root
        self.flow_specs = flow_specs

        self.graph = nx.Graph()

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

    def add_bridges(self):
        bridge_dict= {"bridge_name": "br0",
                     "switch_IP": "192.168.1.101",
                     "usr": "admin",
                     "psswd": "password"}

        self.graph.add_node(bridge_dict["bridge_name"], node_type="bridge", b=bridge_dict)

        bridge_dict = {"bridge_name": "br1",
                       "switch_IP": "192.168.1.101",
                       "usr": "admin",
                       "psswd": "password"}

        self.graph.add_node(bridge_dict["bridge_name"], node_type="bridge", b=bridge_dict)

        bridge_dict = {"bridge_name": "br2",
                       "switch_IP": "192.168.1.101",
                       "usr": "admin",
                       "psswd": "password"}

        self.graph.add_node(bridge_dict["bridge_name"], node_type="bridge", b=bridge_dict)

        bridge_dict = {"bridge_name": "of-switch",
                       "switch_IP": "192.168.1.101",
                       "usr": "admin",
                       "psswd": "password"}

        self.graph.add_node(bridge_dict["bridge_name"], node_type="bridge", b=bridge_dict)

    def add_host_nodes(self):

        host_dict = {"host_name": "e5",
                     "host_IP": "192.168.1.10",
                     "mgmt_ip": "10.194.215.232",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:7a:19:e5"}

        self.graph.add_node(host_dict["host_name"], node_type="host", h=host_dict)

        host_dict = {"host_name": "7e",
                     "host_IP": "192.168.1.20",
                     "mgmt_ip": "10.194.179.16",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:8b:02:7e"}

        self.graph.add_node(host_dict["host_name"], node_type="host", h=host_dict)

        host_dict = {"host_name": "66",
                     "host_IP": "192.168.1.30",
                     "mgmt_ip": "10.195.162.179",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:4b:c7:66"}

        self.graph.add_node(host_dict["host_name"], node_type="host", h=host_dict)

        host_dict = {"host_name": "38",
                     "host_IP": "192.168.1.40",
                     "mgmt_ip": "10.193.214.117",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:6b:f7:38"}

        self.graph.add_node(host_dict["host_name"], node_type="host", h=host_dict)


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

    def add_bridge_links(self):

        bridge_to_bridge_bw = 1000000 * 1000 * 10  # Assume pi to switch bandwidth is 10 Gbps
        bridge_to_bridge_delay = 10e-9 * 10  # Assumes pi to switch latency is 10 nanoseconds

        link_dict = {"bridge1": "of-switch",
                     "bridge1_port": "ge-1/1/45",
                     "bridge2": "br0",
                     "node2_port": "ge-1/1/29",
                     "bw": bridge_to_bridge_bw,
                     "delay": bridge_to_bridge_delay}

        self.graph.add_edge(link_dict["bridge1"],
                            link_dict["bridge2"],
                            l=link_dict)

        link_dict = {"bridge1": "br0",
                     "bridge1_port": "ge-1/1/27",
                     "bridge2": "br2",
                     "node2_port": "ge-1/1/39",
                     "bw": bridge_to_bridge_bw,
                     "delay": bridge_to_bridge_delay}

        self.graph.add_edge(link_dict["bridge1"],
                            link_dict["bridge2"],
                            l=link_dict)

        link_dict = {"bridge1": "of-switch",
                     "bridge1_port": "ge-1/1/47",
                     "bridge2": "br1",
                     "node2_port": "ge-1/1/35",
                     "bw": bridge_to_bridge_bw,
                     "delay": bridge_to_bridge_delay}

        self.graph.add_edge(link_dict["bridge1"],
                            link_dict["bridge2"],
                            l=link_dict)

        link_dict = {"bridge1": "br1",
                     "bridge1_port": "ge-1/1/33",
                     "bridge2": "br2",
                     "node2_port": "ge-1/1/41",
                     "bw": bridge_to_bridge_bw,
                     "delay": bridge_to_bridge_delay}

        self.graph.add_edge(link_dict["bridge1"],
                            link_dict["bridge2"],
                            l=link_dict)

    def setup_network_configuration(self):

        # These things are needed by network graph...
        self.add_host_nodes()
        self.add_bridges()
        self.add_host_links()
        self.add_bridge_links()


