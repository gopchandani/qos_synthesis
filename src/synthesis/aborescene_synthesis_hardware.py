__author__ = 'Rakesh Kumar'

import networkx as nx
import sys

from collections import defaultdict
from copy import deepcopy
from synthesis.synthesis_lib import SynthesisLib
from model.intent import Intent


class AboresceneSynthesisHardware(object):

    def __init__(self, params):

        self.network_configuration = None
        self.synthesis_lib = None

        self.params = params

        # VLAN tag constitutes 12 bits.
        # We use 2 left most bits for representing the tree_id
        # And the 10 right most bits for representing the destination switch's id
        self.num_bits_for_k = 2
        self.num_bits_for_switches = 10

        # self.apply_group_intents_immediately = params["apply_group_intents_immediately"]

        self.br_intent_lists = defaultdict(defaultdict)

        # As a packet arrives, these are the tables it is evaluated against, in this order:

        # If the packet belongs to a local host, just pop any tags and send it along.
        self.local_mac_forwarding_rules = 0

        # Rules for taking packets arriving from other switches with vlan tags.
        self.other_switch_vlan_tagged_packet_rules = 1

        # If the packet belongs to some other switch, compute the vlan tag based on the destination switch
        # and the tree that would be used and send it along to next table
        self.tree_vlan_tag_push_rules = 2

        # Use the vlan tag as a match and forward using appropriate tree
        self.aborescene_forwarding_rules = 3

    def __str__(self):
        params_str = ''
        for k, v in self.params.items():
            params_str += "_" + str(k) + "_" + str(v)
        return self.__class__.__name__ + params_str

    def compute_shortest_path_tree(self, dst_br):

        spt = nx.DiGraph()

        mdg = self.network_configuration.get_mdg()

        paths = nx.shortest_path(mdg, source=dst_br.node_id)

        for src in paths:

            if src == dst_br.node_id:
                continue

            for i in range(len(paths[src]) - 1):
                spt.add_edge(paths[src][i], paths[src][i+1])

        return spt


    def compute_k_edge_disjoint_aborescenes(self, k, bridge_dict):

        k_ada = []

        mdg = nx.MultiDiGraph(self.network_configuration.graph)

        for node_id in self.network_configuration.graph:
            node_type = self.network_configuration.get_node_type(node_id)

            # Remove all host nodes
            if node_type == "host":
                mdg.remove_node(node_id)

        dst_br_preds = list(mdg.predecessors(bridge_dict["bridge_name"]))
        dst_br_succs = list(mdg.successors(bridge_dict["bridge_name"]))

        # Remove the predecessor edges to dst_br, to make it the "root"
        for pred in dst_br_preds:
            mdg.remove_edge(pred, bridge_dict["bridge_name"])

        # Initially, remove all successors edges of dst_br as well
        for succ in dst_br_succs:
            mdg.remove_edge(bridge_dict["bridge_name"], succ)

        for i in range(k):

            # Assume there are always k edges as the successor of the dst_br, kill all but one
            for j in range(k):
                if i == j:
                    mdg.add_edge(bridge_dict["bridge_name"], dst_br_succs[j])
                else:
                    if mdg.has_edge(bridge_dict["bridge_name"], dst_br_succs[j]):
                        mdg.remove_edge(bridge_dict["bridge_name"], dst_br_succs[j])

            # Compute and store one
            msa = nx.minimum_spanning_arborescence(mdg)
            k_ada.append(msa)

            # If there are predecessors of dst_br now, we could not find k msa, so break
            if len(list(msa.predecessors(bridge_dict["bridge_name"]))) > 0:
                print "Could not find k msa."
                break

            # Remove its arcs from mdg
            for arc in msa.edges():
                mdg.remove_edge(arc[0], arc[1])

        return k_ada

    def compute_br_intent_lists(self, dst_bridge_dict, tree, tree_id):

        dst_node_id = dst_bridge_dict["bridge_name"]

        for src_node_id in tree:

            for pred in tree.predecessors(src_node_id):
                link_port_dict = self.network_configuration.get_link_dict(src_node_id, pred)
                out_port = link_port_dict["node1_port"]

                intent = Intent("primary", None,  "all", out_port)
                intent.tree_id = tree_id

                if src_node_id in self.br_intent_lists:
                    if dst_node_id in self.br_intent_lists[src_node_id]:
                        self.br_intent_lists[src_node_id][dst_node_id].append(intent)
                    else:
                        self.br_intent_lists[src_node_id][dst_node_id] = [intent]
                else:
                    self.br_intent_lists[src_node_id][dst_node_id] = [intent]

    def install_failover_group_vlan_tag_flow(self, src_br, dst_br, k):

        # Tags: as they are applied to packets leaving on a given tree in the failover buckets.
        modified_tags = []
        for i in range(k):
            modified_tags.append(int(dst_br.synthesis_tag) | (i + 1 << self.num_bits_for_switches))

        sw_intent_list = deepcopy(self.br_intent_lists[src_br][dst_br])

        # Push a fail-over group with each bucket containing a modify VLAN tag action,
        # Each one of these buckets represent actions to be applied to send the packet in one tree
        group_id = self.synthesis_lib.push_fast_failover_group_set_vlan_action(src_br.node_id,
                                                                               sw_intent_list,
                                                                               modified_tags)

        # Push a group/vlan_id setting flow rule
        flow_match = deepcopy(sw_intent_list[0].flow_match)
        flow_match["vlan_id"] = int(dst_br.synthesis_tag) | (1 << self.num_bits_for_switches)

        flow = self.synthesis_lib.push_match_per_in_port_destination_instruct_group_flow(
                src_br.node_id,
                self.aborescene_forwarding_rules,
                group_id,
                1,
                flow_match,
                self.apply_group_intents_immediately)

        # Need to install some more rules to handle the IN_PORT as out_port case.
        for adjacent_br_id, link_data in self.network_configuration.get_adjacent_switch_link_data(src_br.node_id):

            sw_intent_list = deepcopy(self.br_intent_lists[src_br][dst_br])

            # If the intent is such that it is sending the packet back out to the adjacent switch...
            if sw_intent_list[1].out_port == link_data.link_ports_dict[src_br.node_id]:

                # Push a fail-over group with each bucket containing a modify VLAN tag action,
                # Each one of these buckets represent actions to be applied to send the packet in one tree

                sw_intent_list[1].in_port = link_data.link_ports_dict[src_br.node_id]
                group_id = self.synthesis_lib.push_fast_failover_group_set_vlan_action(src_br.node_id,
                                                                                       sw_intent_list,
                                                                                       modified_tags)

                # Push a group/vlan_id setting flow rule
                flow_match = deepcopy(sw_intent_list[0].flow_match)
                flow_match["vlan_id"] = int(dst_br.synthesis_tag) | (1 << self.num_bits_for_switches)
                flow_match["in_port"] = link_data.link_ports_dict[src_br.node_id]

                flow = self.synthesis_lib.push_match_per_in_port_destination_instruct_group_flow(
                        src_br.node_id,
                        self.aborescene_forwarding_rules,
                        group_id,
                        2,
                        flow_match,
                        self.apply_group_intents_immediately)

    def install_all_group_vlan_tag_flow(self, src_br, dst_br, k):

        # Tags: as they are applied to packets leaving on a given tree in the failover buckets.
        modified_tag = int(dst_br.synthesis_tag) | (2 << self.num_bits_for_switches)

        sw_intent_list = [self.br_intent_lists[src_br][dst_br][1]]

        # Push a failover group with each bucket containing a modify VLAN tag action,
        # Each one of these buckets represent actions to be applied to send the packet in one tree
        group_id = self.synthesis_lib.push_select_all_group_set_vlan_action(src_br.node_id,
                                                                            sw_intent_list,
                                                                            modified_tag)

        # Push a group/vlan_id setting flow rule
        flow_match = deepcopy(sw_intent_list[0].flow_match)
        flow_match["vlan_id"] = int(dst_br.synthesis_tag) | (2 << self.num_bits_for_switches)

        flow = self.synthesis_lib.push_match_per_in_port_destination_instruct_group_flow(
                src_br.node_id,
                self.aborescene_forwarding_rules,
                group_id,
                1,
                flow_match,
                self.apply_group_intents_immediately)

    def push_br_intent_lists(self, k):

        for src_br_id in self.br_intent_lists:
            for i, dst_br_id in enumerate(self.br_intent_lists[src_br_id]):
                src_bridge_dict = self.network_configuration.get_bridge_dict(src_br_id)
                dst_bridge_dict = self.network_configuration.get_bridge_dict(dst_br_id)

                # Install the rules to put the vlan tags on for hosts that are at this destination switch
                self.push_src_br_vlan_push_intents(src_bridge_dict, dst_bridge_dict, i+1)
                self.install_failover_group_vlan_tag_flow(src_bridge_dict, dst_bridge_dict, k)
                self.install_all_group_vlan_tag_flow(src_bridge_dict, dst_bridge_dict, k)

    def push_src_br_vlan_push_intents(self, src_bridge_dict, dst_bridge_dict, dst_bridge_tag):
        for host_dict in self.network_configuration.bridge_attached_host_dicts(dst_bridge_dict):

            required_vlan_id = dst_bridge_tag | (1 << self.num_bits_for_switches)

            self.synthesis_lib.push_vlan_push_intents(src_bridge_dict,
                                                      host_dict["host_MAC"],
                                                      required_vlan_id,
                                                      self.tree_vlan_tag_push_rules)

    def push_local_mac_forwarding_rules_rules(self, bridge_dict):

        for host_dict in self.network_configuration.bridge_attached_host_dicts(bridge_dict):

            link_dict = self.network_configuration.get_link_dict(bridge_dict["bridge_name"],host_dict["host_name"])
            print link_dict["node1_port"]
            self.synthesis_lib.push_flow_rule_match_dst_mac_action_outport(bridge_dict,
                                                                           host_dict["host_MAC"],
                                                                           link_dict["node1_port"],
                                                                           self.local_mac_forwarding_rules)


    def push_other_switch_vlan_tagged_packet_rules(self, bridge_dict):

        for host_dict in self.network_configuration.bridge_attached_host_dicts(bridge_dict):
            link_dict = self.network_configuration.get_link_dict(bridge_dict["bridge_name"], host_dict["host_name"])
            self.synthesis_lib.push_vlan_tagged_table_jump_rule(bridge_dict,
                                                             self.other_switch_vlan_tagged_packet_rules,
                                                             self.aborescene_forwarding_rules)

    def synthesize_all_switches(self, k):

        for bridge_dict in self.network_configuration.bridge_dict_iter():

            # Push table switch rules
            self.synthesis_lib.push_table_miss_goto_next_table_flow(bridge_dict, self.local_mac_forwarding_rules)
            self.synthesis_lib.push_table_miss_goto_next_table_flow(bridge_dict, self.other_switch_vlan_tagged_packet_rules)
            self.synthesis_lib.push_table_miss_goto_next_table_flow(bridge_dict, self.tree_vlan_tag_push_rules)
            #


            self.push_other_switch_vlan_tagged_packet_rules(bridge_dict)

            self.push_local_mac_forwarding_rules_rules(bridge_dict)

            k_ada = self.compute_k_edge_disjoint_aborescenes(k, bridge_dict)

            for i in range(k):
                  self.compute_br_intent_lists(bridge_dict, k_ada[i], i+1)


        self.push_br_intent_lists(k)

    def synthesize_flow_specifications(self, flow_specs):
        self.synthesize_all_switches(2)