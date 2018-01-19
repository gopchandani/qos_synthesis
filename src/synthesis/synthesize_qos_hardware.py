uthor__ = 'Rakesh Kumar'

from collections import defaultdict
from copy import deepcopy
import networkx as nx
from model.intent import Intent
import os


class SynthesizeQoSHardware:

    def __init__(self, params):

        self.params = params

        self.network_configuration = None
        self.synthesis_lib = None
        self.mininet_obj = None

        self.primary_path_edges = []
        self.primary_path_edge_dict = {}

        self.apply_tag_intents_immediately = True
        self.apply_other_intents_immediately = True

    def __str__(self):
        params_str = ''
        for k, v in self.params.items():
            params_str += "_" + str(k) + "_" + str(v)
        return self.__class__.__name__ + params_str

    def compute_path_intents(self, fs):

        intent_list = []
        src_host_dict = self.network_configuration.get_host_dict(fs.src_host_id)
        dst_host_dict = self.network_configuration.get_host_dict(fs.dst_host_id)

        fs.path = nx.shortest_path(self.network_configuration.graph,
                                   source=fs.src_host_id,
                                   target=fs.dst_host_id,
                                   weight='weight')

        # Get the port where the host connects at the first switch in the path
        link_ports_dict = self.network_configuration.get_link_dict(fs.src_host_id, src_host_dict["bridge_id"])
        in_port = link_ports_dict["node2_port"]

        # This loop always starts at a switch
        for i in range(1, len(fs.path) - 1):

            # Out port is the port on which the next switch is connected at this switch
            link_ports_dict = self.network_configuration.get_link_dict(fs.path[i], fs.path[i+1])
            out_port = link_ports_dict["node1_port"]

            intent = Intent("primary",
                            None,
                            in_port,
                            out_port,
                            True,
                            min_rate=fs.configured_rate_bps,
                            max_rate=fs.configured_rate_bps)

            intent.src_mac = src_host_dict["host_MAC"]
            intent.dst_mac = dst_host_dict["host_MAC"]

            # Store the switch id in the intent

            intent.min_rate = fs.configured_rate_bps
            intent.max_rate = fs.configured_rate_bps
            intent.bridge_dict = self.network_configuration.get_bridge_dict(link_ports_dict["node1"])

            intent_list.append(intent)
            in_port = link_ports_dict["node2_port"]

        return intent_list

    def synthesize_flow_specifications(self, flow_specs):
        
        print "Synthesizing rules in the switches..."

        intent_list_dict = defaultdict(defaultdict)
        for fs in flow_specs:
            # Compute intents for the path of the fs
            intent_list = self.compute_path_intents(fs)
            intent_list_dict[fs] = intent_list

        for fs in flow_specs:
            # Push intents one by one to the switches
            for intent in intent_list_dict[fs]:
                q_id = self.synthesis_lib.push_queue(intent.bridge_dict,
                                                     intent.out_port,
                                                     intent.min_rate,
                                                     intent.max_rate)

                self.synthesis_lib.push_flow(intent.bridge_dict,
                                             intent.out_port,
                                             intent.src_mac,
                                             intent.dst_mac,
                                             q_id)
