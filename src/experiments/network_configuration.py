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
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.link import TCIntf, TCLink

from mininet.util import custom
from model.network_graph import NetworkGraph
from model.match import Match

from experiments.topologies.ring_topo import RingTopo
from experiments.topologies.clos_topo import ClosTopo
from experiments.topologies.linear_topo import LinearTopo
from experiments.topologies.linear_modified_topo import LinearModifiedTopo
from experiments.topologies.fat_tree import FatTree
from experiments.topologies.two_ring_topo import TwoRingTopo
from experiments.topologies.ring_line_topo import RingLineTopo
from experiments.topologies.clique_topo import CliqueTopo
from experiments.topologies.ameren_topo import AmerenTopo

from synthesis.dijkstra_synthesis import DijkstraSynthesis
from synthesis.aborescene_synthesis import AboresceneSynthesis
from synthesis.synthesize_qos import SynthesizeQoS
from synthesis.synthesis_lib import SynthesisLib


class NetworkConfiguration(object):

    def __init__(self, controller,
                 topo_name,
                 topo_params,
                 conf_root,
                 synthesis_name,
                 synthesis_params):

        self.controller = controller
        self.topo_name = topo_name
        self.topo_params = topo_params
        self.topo_name = topo_name
        self.conf_root = conf_root
        self.synthesis_name = synthesis_name
        self.synthesis_params = synthesis_params

        self.controller_port = 6633
        self.topo = None
        self.nc_topo_str = None
        self.init_topo()
        self.init_synthesis()

        self.mininet_obj = None
        self.ng = None

        # Setup the directory for saving configs, check if one does not exist,
        # if not, assume that the controller, mininet and rule synthesis needs to be triggered.
        self.conf_path = self.conf_root + str(self) + "/"
        if not os.path.exists(self.conf_path):
            os.makedirs(self.conf_path)
            self.load_config = False
            self.save_config = True
        else:
            self.load_config = True
            self.save_config = False

        #
        # self.load_config = False
        # self.save_config = True

        # Initialize things to talk to controller
        self.baseUrlRyu = "http://localhost:8080/"

        self.h = httplib2.Http(".cache")
        self.h.add_credentials('admin', 'admin')

    def __str__(self):
        return self.controller + "_" + str(self.synthesis) + "_" + str(self.topo)

    def init_topo(self):
        if self.topo_name == "ring":
            self.topo = RingTopo(self.topo_params)
            self.nc_topo_str = "Ring topology with " + str(self.topo.total_switches) + " switches"
        elif self.topo_name == "clostopo":
            self.topo = ClosTopo(self.topo_params)
            self.nc_topo_str = "Clos topology with " + str(self.topo.total_switches) + " switches"
        elif self.topo_name == "linear_modified":
            self.topo = LinearModifiedTopo(self.topo_params)
            self.nc_topo_str = "linear_modified topology with " + str(self.topo_params["num_switches"]) + " switches"
        else:
            raise NotImplementedError("Topology: %s" % self.topo_name)

    def init_synthesis(self):
        if self.synthesis_name == "DijkstraSynthesis":
            self.synthesis_params["master_switch"] = self.topo_name == "linear_modified"
            self.synthesis = DijkstraSynthesis(self.synthesis_params)

        elif self.synthesis_name == "SynthesizeQoS":
            self.synthesis = SynthesizeQoS(self.synthesis_params)

        elif self.synthesis_name == "AboresceneSynthesis":
            self.synthesis = AboresceneSynthesis(self.synthesis_params)

    def test_synthesis(self):

        self.mininet_obj.pingAll()

        # is_bi_connected = self.is_bi_connected_manual_ping_test_all_hosts()

        # is_bi_connected = self.is_bi_connected_manual_ping_test([(self.mininet_obj.get('h11'), self.mininet_obj.get('h31'))])

        # is_bi_connected = self.is_bi_connected_manual_ping_test([(self.mininet_obj.get('h31'), self.mininet_obj.get('h41'))],
        #                                                            [('s1', 's2')])
        # print "is_bi_connected:", is_bi_connected

    def get_ryu_switches(self):
        ryu_switches = {}
        request_gap = 0

        # Get all the ryu_switches from the inventory API
        remaining_url = 'stats/switches'
        time.sleep(request_gap)
        resp, content = self.h.request(self.baseUrlRyu + remaining_url, "GET")

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

        mininet_host_nodes = {}

        for sw in self.topo.switches():
            mininet_host_nodes[sw] = []
            for h in self.get_all_switch_hosts(sw):
                mininet_host_dict = {"host_switch_id": "s" + sw[1:],
                                     "host_name": h.name,
                                     "host_IP": h.IP(),
                                     "host_MAC": h.MAC()}

                mininet_host_nodes[sw].append(mininet_host_dict)

        with open(self.conf_path + "mininet_host_nodes.json", "w") as outfile:
            json.dump(mininet_host_nodes, outfile)

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

    def setup_network_graph(self, mininet_setup_gap=None, synthesis_setup_gap=None):

        self.start_mininet()
        if mininet_setup_gap:
            time.sleep(mininet_setup_gap)

        # These things are needed by network graph...
        self.get_host_nodes()
        self.get_links()
        self.get_switches()

        self.ng = NetworkGraph(network_configuration=self)
        self.ng.parse_network_graph()

        # Now the synthesis...
        if synthesis_setup_gap:
            time.sleep(synthesis_setup_gap)

        # Refresh just the switches in the network graph, post synthesis
        self.get_switches()
        self.ng.parse_switches()

        # TODO: Figure out a new home for these two
        self.synthesis.network_graph = self.ng
        self.synthesis.mininet_obj = self.mininet_obj
        self.synthesis.synthesis_lib = SynthesisLib("localhost", "8181", self.ng)

        return self.ng

    def start_mininet(self):

        self.cleanup_mininet()

        intf = custom(TCIntf, bw=1000)

        self.topo.addLink("s1", "s2", bw=10, delay='5m', use_htb=True)

        self.mininet_obj = Mininet(topo=self.topo,
                                   intf=TCIntf,
                                   link=TCLink,
                                   cleanup=True,
                                   autoStaticArp=True,
                                   controller=lambda name: RemoteController(name, ip='127.0.0.1',
                                                                            port=self.controller_port),
                                   switch=partial(OVSSwitch, protocols='OpenFlow14'))

        self.mininet_obj.start()

    def cleanup_mininet(self):

        if self.mininet_obj:
            print "Mininet cleanup..."
            #self.mininet_obj.stop()

        os.system("sudo mn -c")

    def get_all_switch_hosts(self, switch_id):

        p = self.topo.ports

        for node in p:

            # Only look for this switch's hosts
            if node != switch_id:
                continue

            for switch_port in p[node]:
                dst_list = p[node][switch_port]
                dst_node = dst_list[0]
                if dst_node.startswith("h"):
                    yield self.mininet_obj.get(dst_node)

    def _get_experiment_host_pair(self):

        for src_switch in self.topo.get_switches_with_hosts():
            for dst_switch in self.topo.get_switches_with_hosts():
                if src_switch == dst_switch:
                    continue

                # Assume one host per switch
                src_host = "h" + src_switch[1:] + "1"
                dst_host = "h" + dst_switch[1:] + "1"

                src_host_node = self.mininet_obj.get(src_host)
                dst_host_node = self.mininet_obj.get(dst_host)

                yield (src_host_node, dst_host_node)

    def is_host_pair_pingable(self, src_host, dst_host):
        hosts = [src_host, dst_host]
        ping_loss_rate = self.mininet_obj.ping(hosts, '1')

        # If some packets get through, then declare pingable
        if ping_loss_rate < 100.0:
            return True
        else:
            # If not, do a double check:
            cmd_output = src_host.cmd("ping -c 3 " + dst_host.IP())
            print cmd_output
            if cmd_output.find("0 received") != -1:
                return False
            else:
                return True

    def are_all_hosts_pingable(self):
        ping_loss_rate = self.mininet_obj.pingAll('1')

        # If some packets get through, then declare pingable
        if ping_loss_rate < 100.0:
            return True
        else:
            return False
