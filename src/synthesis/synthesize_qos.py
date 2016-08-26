__author__ = 'Rakesh Kumar'

import os

from collections import defaultdict
from copy import deepcopy
import networkx as nx
from model.intent import Intent


class SynthesizeQoS:

    def __init__(self, params):

        self.params = params

        self.network_graph = None
        self.synthesis_lib = None

        self.primary_path_edges = []
        self.primary_path_edge_dict = {}

        self.apply_tag_intents_immediately = True
        self.apply_other_intents_immediately = True

        # Table contains any rules that have to do with vlan tag push
        self.vlan_tag_push_rules_table_id = 0

        # Table contains any rules associated with forwarding host traffic
        self.mac_forwarding_table_id = 1

        # Table contains the actual forwarding rules
        self.vlan_forwarding_table_id = 2

        self.ifb_interfaces_used = 0

    def __str__(self):
        params_str = ''
        for k, v in self.params.items():
            params_str += "_" + str(k) + "_" + str(v)
        return self.__class__.__name__ + params_str

    def init_ifb(self, num_ifb_interfaces):
        os.system("sudo modprobe -r ifb")
        os.system("sudo modprobe ifb numifbs=" + str(num_ifb_interfaces))
        os.system("sudo modprobe act_mirred")
        os.system("sudo modprobe sch_fq_codel")

    def compute_path_intents(self, src_host, dst_host, p, intent_type,
                                 flow_match, first_in_port, dst_switch_tag, rate):

        edge_ports_dict = self.network_graph.get_link_ports_dict(p[0], p[1])

        in_port = first_in_port
        out_port = edge_ports_dict[p[0]]

        # This loop always starts at a switch
        for i in range(len(p) - 1):

            fwd_flow_match = deepcopy(flow_match)

            if not self.params["same_output_queue"]:
                mac_int = int(dst_host.mac_addr.replace(":", ""), 16)
                fwd_flow_match["ethernet_destination"] = int(mac_int)

            intent = Intent(intent_type,
                            fwd_flow_match,
                            in_port,
                            out_port,
                            self.apply_other_intents_immediately,
                            min_rate=rate,
                            max_rate=rate)

            # Using dst_switch_tag as key here to
            # avoid adding multiple intents for the same destination
            if self.params["same_output_queue"]:
                self.add_intent(p[i], dst_switch_tag, intent)
            else:
                self.add_intent(p[i], (dst_switch_tag, dst_host.mac_addr), intent)

            # Prep for next switch
            if i < len(p) - 2:
                edge_ports_dict = self.network_graph.get_link_ports_dict(p[i], p[i + 1])
                in_port = edge_ports_dict[p[i+1]]

                edge_ports_dict = self.network_graph.get_link_ports_dict(p[i + 1], p[i + 2])
                out_port = edge_ports_dict[p[i+1]]

    def get_intents(self, dst_intents, intent_type):

        return_intent = []

        for intent in dst_intents:
            if intent.intent_type == intent_type:
                return_intent.append(intent)

        return return_intent

    def add_intent(self, switch_id, key, intent):

        intents = self.network_graph.graph.node[switch_id]["sw"].intents

        if key in intents:
            intents[key][intent] += 1
        else:
            intents[key] = defaultdict(int)
            intents[key][intent] = 1

    def compute_destination_host_mac_intents(self, h_obj, flow_match, matching_tag, rate):

        edge_ports_dict = self.network_graph.get_link_ports_dict(h_obj.sw.node_id, h_obj.node_id)
        out_port = edge_ports_dict[h_obj.sw.node_id]

        host_mac_match = deepcopy(flow_match)
        mac_int = int(h_obj.mac_addr.replace(":", ""), 16)
        host_mac_match["ethernet_destination"] = int(mac_int)
        host_mac_match["vlan_id"] = int(matching_tag)

        host_mac_intent = Intent("mac", host_mac_match, "all", out_port,
                                 self.apply_other_intents_immediately,
                                 min_rate=rate, max_rate=rate)

        # Avoiding addition of multiple mac forwarding intents for the same host 
        # by using its mac address as the key
        self.add_intent(h_obj.sw.node_id, h_obj.mac_addr, host_mac_intent)

    def install_ingress_ifb_filter(self, h_obj, rate):

        # Get the interface name where the host is connected
        orig_intf_name = h_obj.sw.node_id + "-eth" + str(h_obj.switch_port.port_number)

        # Map a mirror ifb interface for this interface
        ifb_intf_name = "ifb" + str(self.ifb_interfaces_used)

        # Set some options for this interface name
        os.system("sudo ethtool -K " + orig_intf_name + " tso off gso off gro off")

        # Remove previous tc stuff on both of these interfaces
        os.system("tc qdisc del dev " + orig_intf_name + " root")
        os.system("tc qdisc del dev " + orig_intf_name + " ingress")
        os.system("tc qdisc del dev " + ifb_intf_name + " root")
        os.system("tc qdisc del dev " + ifb_intf_name + " ingress")

        os.system("tc qdisc add dev " + orig_intf_name + " handle ffff: ingress")

        os.system("ifconfig " + ifb_intf_name + " up")

        cmd = "tc filter add dev " + orig_intf_name + \
              " parent ffff: protocol all u32 match u32 0 0 action mirred egress redirect dev " + ifb_intf_name

        os.system(cmd)
        self.ifb_interfaces_used += 1

        # Create an EGRESS filter on the IFB device
        os.system("tc qdisc add dev " + ifb_intf_name + " root handle 1: htb default 11")

        # Add root class HTB with rate limiting
        os.system("tc class add dev " + ifb_intf_name + " parent 1: classid 1:1 htb rate " + str(rate) + "bit")
        os.system("tc class add dev " + ifb_intf_name + " parent 1:1 classid 1:11 htb rate " + str(rate) + "bit" + " prio 0 quantum 1514")

        # Add FQ_CODEL qdisc with ECN support (if you want ecn)
        os.system("tc qdisc add dev " + ifb_intf_name + " parent 1:11 fq_codel quantum 1514 ecn")




        # # Configure a tbf qdisc on the ingress interface
        # os.system("tc qdisc add dev " + ifb_intf_name + " root tbf rate " + str(rate) + "bit latency 50ms burst 1540")
        # print "Installed ifb interface named:", ifb_intf_name, "for interface:", orig_intf_name, "rate:", rate

    def compute_push_vlan_tag_intents(self, h_obj, flow_match, required_tag):

        push_vlan_match= deepcopy(flow_match)
        push_vlan_match["in_port"] = int(h_obj.switch_port.port_number)
        push_vlan_tag_intent = Intent("push_vlan", push_vlan_match, h_obj.switch_port.port_number, "all",
                                      self.apply_tag_intents_immediately)

        push_vlan_tag_intent.required_vlan_id = required_tag

        # Avoiding adding a new intent for every departing flow for this switch,
        # by adding the tag as the key

        self.add_intent(h_obj.sw.node_id, required_tag, push_vlan_tag_intent)

    def synthesize_flow_qos(self, fs):

        # Handy info
        edge_ports_dict = self.network_graph.get_link_ports_dict(fs.src_host.node_id, fs.src_host.sw.node_id)
        in_port = edge_ports_dict[fs.src_host.sw.node_id]

        # Things at source
        # Tag packets leaving the source host with a vlan tag of the destination switch
        self.compute_push_vlan_tag_intents(fs.src_host, fs.flow_match, fs.dst_host.sw.synthesis_tag)

        # Things at destination
        # Add a MAC based forwarding rule for the destination host at the last hop
        self.compute_destination_host_mac_intents(fs.dst_host, fs.flow_match, fs.dst_host.sw.synthesis_tag, fs.send_rate_bps)

        #  First find the shortest path between src and dst.
        p = nx.shortest_path(self.network_graph.graph, source=fs.src_host.sw.node_id, target=fs.dst_host.sw.node_id)
        print "Primary Path:", p

        self.primary_path_edge_dict[(fs.src_host.node_id, fs.dst_host.node_id)] = []

        for i in range(len(p)-1):

            if (p[i], p[i+1]) not in self.primary_path_edges and (p[i+1], p[i]) not in self.primary_path_edges:
                self.primary_path_edges.append((p[i], p[i+1]))

            self.primary_path_edge_dict[(fs.src_host.node_id, fs.dst_host.node_id)].append((p[i], p[i+1]))

        #  Compute all forwarding intents as a result of primary path
        self.compute_path_intents(fs.src_host, fs.dst_host, p, "primary", fs.flow_match, in_port,
                                     fs.dst_host.sw.synthesis_tag, fs.send_rate_bps)

    def push_switch_changes(self):

        # Install ingress filters for each possible src in flow_specifications
        hosts_rates_for_ifb = []
        for fs in self.flow_specifications:
            if (fs.src_host, fs.send_rate_bps) not in hosts_rates_for_ifb:
                hosts_rates_for_ifb.append((fs.src_host, fs.send_rate_bps))

        self.init_ifb(len(hosts_rates_for_ifb))
        for src_host, send_rate_bps in hosts_rates_for_ifb:
            self.install_ingress_ifb_filter(src_host, send_rate_bps)

        for sw in self.network_graph.get_switches():

            print "-- Pushing at Switch:", sw.node_id

            # Push table miss entries at all Tables
            self.synthesis_lib.push_table_miss_goto_next_table_flow(sw.node_id, 0)
            self.synthesis_lib.push_table_miss_goto_next_table_flow(sw.node_id, 1)
            self.synthesis_lib.push_table_miss_goto_next_table_flow(sw.node_id, 2)

            for dst in sw.intents:
                dst_intents = sw.intents[dst]

                # Take care of mac intents for this destination
                self.synthesis_lib.push_destination_host_mac_intents(sw.node_id,
                                                                     self.get_intents(dst_intents, "mac"),
                                                                     self.mac_forwarding_table_id)

                # Take care of vlan tag push intents for this destination
                self.synthesis_lib.push_vlan_push_intents(sw.node_id,
                                                          self.get_intents(dst_intents, "push_vlan"),
                                                          self.vlan_tag_push_rules_table_id)

                primary_intents = self.get_intents(dst_intents, "primary")

                #  Handle the case when the switch does not have to carry any failover traffic
                if primary_intents:

                    combined_intent = deepcopy(primary_intents[0])

                    if self.params["same_output_queue"]:
                        combined_intent.min_rate = 0
                        combined_intent.max_rate = 0

                        for primary_intent in primary_intents:
                            combined_intent.min_rate += primary_intent.min_rate
                            combined_intent.max_rate += primary_intent.max_rate

                    group_id = self.synthesis_lib.push_select_all_group(sw.node_id, [combined_intent])

                    flow = self.synthesis_lib.push_match_per_in_port_destination_instruct_group_flow(
                            sw.node_id,
                            self.vlan_forwarding_table_id,
                            group_id,
                            1,
                            combined_intent.flow_match,
                            combined_intent.apply_immediately)

    def synthesize_flow_specifications(self, flow_specifications):

        self.flow_specifications = flow_specifications

        for fs in flow_specifications:

            # Ignore paths with same src/dst
            if fs.src_host == fs.dst_host:
                continue

            # Ignore installation of paths between switches on the same switch
            if fs.src_host.sw.node_id == fs.dst_host.sw.node_id:
                continue

            self.synthesize_flow_qos(fs)

            print "-----------------------------------------------------------------------------------------------"

        self.push_switch_changes()
