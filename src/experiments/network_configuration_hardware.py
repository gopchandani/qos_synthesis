__author__ = 'Rakesh Kumar'

import time
import os
import json
import httplib2
import fcntl
import struct
from socket import *

from collections import defaultdict
from functools import partial
from model.network_graph import NetworkGraph
from model.match import Match

from synthesis.dijkstra_synthesis import DijkstraSynthesis
from synthesis.aborescene_synthesis import AboresceneSynthesis
from synthesis.synthesize_qos_hardware import SynthesizeQoS
from synthesis.synthesis_lib import SynthesisLib


class NetworkConfiguration(object):

    def __init__(self, controller,
                 conf_root,
                 synthesis_name,
                 synthesis_params,
                 flow_specs):

        self.controller = controller
        self.conf_root = conf_root
        self.synthesis_name = synthesis_name
        self.synthesis_params = synthesis_params
        self.flow_specs = flow_specs

        self.controller_port = 6666
        self.nc_topo_str = None
        self.init_synthesis()

        self.ng = None

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

    def init_synthesis(self):
        if self.synthesis_name == "DijkstraSynthesis":
            self.synthesis_params["master_switch"] = True
            self.synthesis = DijkstraSynthesis(self.synthesis_params)

        elif self.synthesis_name == "SynthesizeQoS":
            self.synthesis = SynthesizeQoS(self.synthesis_params)

        elif self.synthesis_name == "AboresceneSynthesis":
            self.synthesis = AboresceneSynthesis(self.synthesis_params)

    def get_ryu_switches(self):
        ryu_switches = {}
        request_gap = 0

        # Get all the ryu_switches from the inventory API
        remaining_url = 'stats/switches'
        time.sleep(request_gap)
        resp, content = self.h.request(self.baseUrlRyu + remaining_url, "GET")
        print resp

        ryu_switch_numbers = json.loads(content)

        for dpid in ryu_switch_numbers:

            this_ryu_switch = {}

            # Get the flows
            remaining_url = 'stats/flow' + "/" + str(dpid)
            resp, content = self.h.request(self.baseUrlRyu + remaining_url, "GET")
            time.sleep(request_gap)

            if resp["status"] == "200":
                switch_flows = json.loads(content)
                switch_flow_tables = defaultdict(list)
                for flow_rule in switch_flows[str(dpid)]:
                    switch_flow_tables[flow_rule["table_id"]].append(flow_rule)
                this_ryu_switch["flow_tables"] = switch_flow_tables
            else:
                print "Error pulling switch flows from RYU."

            # Get the ports
            remaining_url = 'stats/portdesc' + "/" + str(dpid)
            resp, content = self.h.request(self.baseUrlRyu + remaining_url, "GET")
            time.sleep(request_gap)

            if resp["status"] == "200":
                switch_ports = json.loads(content)
                this_ryu_switch["ports"] = switch_ports[str(dpid)]
            else:
                print "Error pulling switch ports from RYU."

            # Get the groups
            remaining_url = 'stats/groupdesc' + "/" + str(dpid)
            resp, content = self.h.request(self.baseUrlRyu + remaining_url, "GET")
            time.sleep(request_gap)

            if resp["status"] == "200":
                switch_groups = json.loads(content)
                this_ryu_switch["groups"] = switch_groups[str(dpid)]
            else:
                print "Error pulling switch ports from RYU."

            ryu_switches[dpid] = this_ryu_switch

        with open(self.conf_path + "ryu_switches.json", "w") as outfile:
            json.dump(ryu_switches, outfile)

    def get_host_nodes(self):

        self.h_hosts = {}
        host_nodes = {}

        sw = "s2347862419956695048"
        host_nodes[sw] = []
        host_dict = {"host_switch_id": "s" + sw[1:],
                     "host_name": "38",
                     "host_IP": "192.168.0.1",
                     "mgmt_ip": "10.195.229.241",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:6b:f7:38"}

        self.h_hosts[host_dict["host_name"]] = host_dict

        host_nodes[sw].append(host_dict)

        host_dict = {"host_switch_id": "s" + sw[1:],
                     "host_name": "e5",
                     "host_IP": "192.168.0.2",
                     "mgmt_ip": "10.194.45.219",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:7a:19:e5"}

        self.h_hosts[host_dict["host_name"]] = host_dict

        host_nodes[sw].append(host_dict)

        sw = "s2347862419956695105"
        host_nodes[sw] = []

        host_dict = {"host_switch_id": "s" + sw[1:],
                     "host_name": "66",
                     "host_IP": "192.168.0.3",
                     "mgmt_ip": "10.195.36.116",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:4b:c7:66"}

        self.h_hosts[host_dict["host_name"]] = host_dict

        host_nodes[sw].append(host_dict)

        host_dict = {"host_switch_id": "s" + sw[1:],
                     "host_name": "7e",
                     "host_IP": "192.168.0.4",
                     "mgmt_ip": "10.195.161.97",
                     "usr": "pi",
                     "psswd": "raspberry",
                     "host_MAC": "b8:27:eb:8b:02:7e"}

        self.h_hosts[host_dict["host_name"]] = host_dict

        host_nodes[sw].append(host_dict)
	
        with open(self.conf_path + "mininet_host_nodes.json", "w") as outfile:
            json.dump(host_nodes, outfile)

        return host_nodes

    def get_links(self):

        mininet_port_links = {}

        mininet_port_links["38"] = {"0": ["s2347862419956695048", 47]}
        mininet_port_links["e5"] = {"0": ["s2347862419956695048", 43]}
        mininet_port_links["s2347862419956695048"] = {"47": ["38", 47],
                                                      "43": ["e5", 43],
                                                      "45": ["s2347862419956695105", 45]}
        # mininet_port_links["s1"] = {"1": ["7e", 0], "2": ["e5", 0], "174": ["s2", 174]}

        mininet_port_links["66"] = {"0": ["s2347862419956695105", 47]}
        mininet_port_links["7e"] = {"0": ["s2347862419956695105", 43]}
        mininet_port_links["s2347862419956695105"] = {"47": ["66", 47],
                                                      "43": ["7e", 43],
                                                      "45": ["s2347862419956695048", 45]}
        # mininet_port_links["66"] = {"0": ["s2", 1]}
        # mininet_port_links["38"] = {"0": ["s2", 2]}
        # mininet_port_links["s2"] = {"1": ["66", 0], "2": ["38", 0], "174": ["s1", 174]}

        with open(self.conf_path + "mininet_port_links.json", "w") as outfile:
            json.dump(mininet_port_links, outfile)

        return mininet_port_links

    def get_link_params(self):

        mininet_link_params = []

        mininet_link_params.append({"node1": "38", "delay": "3ms", "node2": "s2347862419956695048", "bw": 5})
        mininet_link_params.append({"node1": "e5", "delay": "3ms", "node2": "s2347862419956695048", "bw": 5})
        mininet_link_params.append({"node1": "s2347862419956695048", "delay": "3ms", "node2": "s2347862419956695105", "bw": 5})
        mininet_link_params.append({"node1": "66", "delay": "3ms", "node2": "s2347862419956695105", "bw": 5})
        mininet_link_params.append({"node1": "7e", "delay": "3ms", "node2": "s2347862419956695105", "bw": 5})
        # mininet_link_params.append({"node1": "66", "delay": "3ms", "node2": "s2", "bw": 5})
        # mininet_link_params.append({"node1": "38", "delay": "3ms", "node2": "s2", "bw": 5})

        with open(self.conf_path + "mininet_link_params.json", "w") as outfile:
            json.dump(mininet_link_params, outfile)

        return mininet_link_params

    def get_switches(self):
        # Now the output of synthesis is carted away
        if self.controller == "ryu" or self.controller == "ryu_old":
            self.get_ryu_switches()
        else:
            raise NotImplemented

    def init_flow_specs(self):
        for fs in self.flow_specs:
            fs.ng_src_host = self.ng.get_node_object(fs.src_host_id)
            fs.ng_dst_host = self.ng.get_node_object(fs.dst_host_id)

    def setup_network_graph(self, mininet_setup_gap=None, synthesis_setup_gap=None):

        # These things are needed by network graph...
        self.get_host_nodes()
        self.get_links()
        self.get_link_params()
        self.get_switches()

        self.ng = NetworkGraph(network_configuration=self)
        self.ng.parse_network_graph()

        # TODO: Figure out a new home for these two
        self.synthesis.network_graph = self.ng
        self.synthesis.synthesis_lib = SynthesisLib("192.168.1.102", "8080", self.ng)

        return self.ng

