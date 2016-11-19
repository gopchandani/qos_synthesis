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
from synthesis.synthesize_qos import SynthesizeQoS
from synthesis.synthesis_lib import SynthesisLib

# mhasan import: networkx
import networkx as nx
import sys


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

        self.controller_port = 6633
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
        self.baseUrlRyu = "http://localhost:8080/"

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

        print ryu_switches

    def get_host_nodes(self):

        host_nodes = {}
	sw = "s1"
        host_nodes[sw] = []
        host_dict = {"host_switch_id": "s" + sw[1:],
                     "host_name": "h1s1",
                     "host_IP": h.IP(),
                     "host_MAC": h.MAC()}

        host_nodes[sw].append(host_dict)

        host_dict = {"host_switch_id": "s" + sw[1:],
                     "host_name": h.name,
                     "host_IP": h.IP(),
                     "host_MAC": h.MAC()}

        host_nodes[sw].append(host_dict)
	
	sw = "s2"
        host_nodes[sw] = []
        host_dict = {"host_switch_id": "s" + sw[1:],
                     "host_name": h.name,
                     "host_IP": h.IP(),
                     "host_MAC": h.MAC()}

        host_nodes[sw].append(host_dict)

        host_dict = {"host_switch_id": "s" + sw[1:],
                     "host_name": h.name,
                     "host_IP": h.IP(),
                     "host_MAC": h.MAC()}

        host_nodes[sw].append(host_dict)
	
        with open(self.conf_path + "host_nodes.json", "w") as outfile:
            json.dump(host_nodes, outfile)

        return mininet_host_nodes

    def get_links(self):

        mininet_port_links = {}

        with open(self.conf_path + "mininet_port_links.json", "w") as outfile:
            json.dump(self.topo.ports, outfile)

        return mininet_port_links

    def get_switches(self):
        # Now the output of synthesis is carted away
        if self.controller == "ryu":
            self.get_ryu_switches()
        else:
            raise NotImplemented

    def init_flow_specs(self):
        for fs in self.flow_specs:
            fs.ng_src_host = self.ng.get_node_object(fs.src_host_id)
            fs.ng_dst_host = self.ng.get_node_object(fs.dst_host_id)

    def setup_network_graph(self, mininet_setup_gap=None, synthesis_setup_gap=None):

        # These things are needed by network graph...
        #self.get_host_nodes()
        #self.get_links()
        self.get_switches()

        self.ng = NetworkGraph(network_configuration=self)
        self.ng.parse_network_graph()

        # TODO: Figure out a new home for these two
        self.synthesis.network_graph = self.ng
        self.synthesis.synthesis_lib = SynthesisLib("localhost", "8181", self.ng)

        return self.ng

