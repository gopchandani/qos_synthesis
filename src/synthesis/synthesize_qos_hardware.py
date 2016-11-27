uthor__ = 'Rakesh Kumar'

from collections import defaultdict
from copy import deepcopy
import networkx as nx
from model.intent import Intent


class SynthesizeQoS:

    def __init__(self, params):

        self.params = params

        self.network_graph = None
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

        fs.path = nx.shortest_path(self.network_graph.graph,
                                   source=fs.ng_src_host.node_id,
                                   target=fs.ng_dst_host.node_id,
                                   weight='weight')

        # Get the port where the host connects at the first switch in the path
        link_ports_dict = self.network_graph.get_link_ports_dict(fs.ng_src_host.node_id, fs.ng_src_host.sw.node_id)
        in_port = link_ports_dict[fs.ng_src_host.sw.node_id]

        # This loop always starts at a switch
        for i in range(1, len(fs.path) - 1):

            link_ports_dict = self.network_graph.get_link_ports_dict(fs.path[i], fs.path[i+1])

            fwd_flow_match = deepcopy(fs.flow_match)

            mac_int = int(fs.ng_src_host.mac_addr.replace(":", ""), 16)
            fwd_flow_match["ethernet_source"] = int(mac_int)

            mac_int = int(fs.ng_dst_host.mac_addr.replace(":", ""), 16)
            fwd_flow_match["ethernet_destination"] = int(mac_int)

            intent = Intent("primary",
                            fwd_flow_match,
                            in_port,
                            link_ports_dict[fs.path[i]],
                            True)

            # Store the switch id in the intent
            intent.switch_id = fs.path[i]

            intent_list.append(intent)
            in_port = link_ports_dict[fs.path[i+1]]

        return intent_list

    def synthesize_flow_specifications(self, flow_specs):
        
        print "Synthesizing rules in the switches..."

        for fs in flow_specs:

            # Compute intents for the path of the fs
            intent_list = self.compute_path_intents(fs)

            # Push intents one by one to the switches
            for intent in intent_list:
                self.synthesis_lib.push_destination_host_mac_intent_flow(intent.switch_id, intent, 0, 100)

