__author__ = 'Rakesh Kumar'

import pprint
import time
import httplib2
import json
import os
import sys

from collections import defaultdict


class SynthesisLibHardware(object):

    def __init__(self, network_configuration):

        self.network_configuration = network_configuration

        self.group_id_cntr = 0
        self.flow_id_cntr = 0
        self.queue_id_cntr = 0

        self.synthesized_primary_paths = defaultdict(defaultdict)
        self.synthesized_failover_paths = defaultdict(defaultdict)

        self.queue_id_cntr_per_br = defaultdict(int)


    def push_flow_rule(self, switch_dict, src_ip, dst_ip, udp_port, out_port, flow_priority, queue_num=0):

        push_flow_cmd = "ovs-ofctl add-flow " + \
                        "tcp:" + str(switch_dict["switch_ip"]) + ":" + str(switch_dict["of_port"]) + " " + \
                        "ip,nw_src=" + str(src_ip) +",nw_dst=" + str(dst_ip) +",udp,tp_dst=" + \
                        str(udp_port) + ",priority=" + str(flow_priority) + \
                        ",actions=set_queue:"+ str(queue_num) + ",output:" + str(out_port.split('/')[2])
        os.system(push_flow_cmd)


    def push_flow_rule_group(self, switch_dict, group_id, src_ip, dst_ip, udp_port, flow_priority):

        push_flow_cmd = "ovs-ofctl -O OpenFlow13 add-flow " + \
                        "tcp:" + str(switch_dict["switch_ip"]) + ":" + str(switch_dict["of_port"]) + " " + \
                        "ip,nw_src=" + str(src_ip) + ",nw_dst=" + str(dst_ip) + \
                        ",udp,tp_dst=" + str(udp_port) + \
                        ",priority=" + str(flow_priority) + ",actions=group:" + str(group_id)

        os.system(push_flow_cmd)

    def push_queue(self, switch_dict, port, min_rate, max_rate, queue_priority):
        min_rate_str = str(min_rate)
        max_rate_str = str(max_rate)

        queue_cmd = "ovs-vsctl " + "--db=tcp:" + str(switch_dict["switch_ip"]) + ":6634 -- " + \
                    "set port " + str(port) + " qos=@newqos -- " + \
                    "--id=@newqos create qos type=PRONTO_STRICT " + \
                    " queues:" + str(queue_priority) + \
                    "=@sample_name -- " + \
                    "--id=@sample_name" + \
                    " create queue other-config:min-rate=" + str(min_rate_str) + \
                    " other-config:max-rate=" + str(max_rate_str)

        os.system(queue_cmd)

    def push_group(self, switch_dict, group_id, group_type, buckets):

        group_command = 'ovs-ofctl -O OpenFlow13 add-group' + ' ' + \
                        'tcp:' + switch_dict['switch_ip'] + ':' + switch_dict['of_port'] + ' ' + \
                        'group_id=' + str(group_id) + ',' + \
                        'type=' + str(group_type) + ',' + \
                        'bucket=watch_port:' + buckets[0]["watch_port"].split('/')[2] + ',' + 'output:' + \
                        buckets[0]["output_port"].split('/')[2] + ',' + \
                        'bucket=watch_port:' + \
                        buckets[1]["watch_port"].split('/')[2] + ',' + \
                        'output:' + buckets[1]["output_port"].split('/')[2]

        os.system(group_command)













    def push_table_miss_goto_next_table_flow(self, bridge_dict, src_table,priority):

        dst_table_id = src_table + 1

        flow_rule = "ovs-ofctl" + " " + \
                    "add-flow " + "tcp:"+ bridge_dict["switch_IP"] + ":" + \
                    bridge_dict["of_port"] + " " + \
                    "table=" + str(src_table)+ "," + \
                    'priority=' + str(priority) + ',' + \
                    "actions=goto_table:" + str(dst_table_id)

        os.system(flow_rule)

    def push_flow_rule_match_dst_mac_action_outport(self,bridge_dict, dst_mac,out_port, table_id,priority):

        flow_rule = "ovs-ofctl" + " " + \
                    "add-flow " + "tcp:"+ bridge_dict["switch_IP"] + ":" + bridge_dict["of_port"] + ": " + \
                    "table=" + str(table_id) + "," + \
                    'priority=' + str(priority) + ',' + \
                    "vlan_vid=0x1000/0x1000" + "," + \
                    "dl_dst=" + dst_mac + "," + \
                    "actions=strip_vlan,output:" + str(out_port.split('/')[2])

        os.system(flow_rule)


    def push_vlan_tagged_table_jump_rule(self, bridge_dict, src_table, dst_table, priority):

        flow_rule = "ovs-ofctl" + " " + \
                    "add-flow " + "tcp:"+ bridge_dict["switch_IP"] + ":" + \
                    bridge_dict["of_port"] + " " + \
                    "table=" + str(src_table) + "," + \
                    'priority=' + str(priority) + ',' + \
                    "vlan_vid=0x1000/0x1000" + "," + \
                    "actions=goto_table:" + str(dst_table)

        os.system(flow_rule)

    def push_vlan_push_intents(self, bridge_dict, dst_host_mac, required_vlan_id, vlan_tag_push_rules_table_id,priority):

        flow_rule = 'ovs-ofctl -O OpenFlow13 add-flow' + ' ' + \
                    'tcp:' + bridge_dict['switch_IP'] + ':' + bridge_dict['of_port'] + ' ' + \
                    'priority=' + str(priority) + ',' + \
                    'dl_dst=' + dst_host_mac + ',' + \
                    'actions=push_vlan:0x8100' + ',mod_vlan_vid:' + str(required_vlan_id) + ',' + \
                    'goto_table:' + str(vlan_tag_push_rules_table_id)


        # TODO: Push a flow rule in the table vlan_tag_push_rules_table_id
        # Match on the dst_host_mac
        # Do three things:
        # 1. Push a vlan tag
        # 2. Set the vlan tag to required_vlan_id
        # 3. Send the packet out to vlan_tag_push_rules_table_id + 1

        # # Compile match
        # flow["match"] = push_vlan_intent.flow_match.generate_match_json(self.network_graph.controller,
        #                                                                 flow["match"])
        #
        # action_list = [{"type": "PUSH_VLAN", "ethertype": 0x8100},
        #                {"type": "SET_FIELD", "field": "vlan_vid", "value": push_vlan_intent.required_vlan_id + 0x1000}]
        #
        # self.populate_flow_action_instruction(flow, action_list, push_vlan_intent.apply_immediately)
        #
        # flow["instructions"].append({"type": "GOTO_TABLE", "table_id": str(vlan_tag_push_rules_table_id + 1)})
        #
        #

        os.system(flow_rule)




    def push_select_all_group_set_vlan_action(self, bridge_dict, intent_list, modified_tag):

        self.group_id_cntr += 1
        group_id = self.group_id_cntr

        group_command = 'ovs-ofctl -O OpenFlow13 add-group' + ' ' \
                        'tcp:' + bridge_dict['switch_IP'] + ':' + bridge_dict['of_port'] + ' ' + \
                        'group_id=' + str(group_id) + ',' + \
                        'type=all' + ',' + \
                        'bucket=actions=mod_vlan_vid:' + str(modified_tag) + ',output:' + \
                        intent_list[0].out_port.split('/')[2] + ',' + \
                        'bucket=actions=mod_vlan_vid:' + str(modified_tag) + ',output:' + \
                        intent_list[1].out_port.split('/')[2]


        # ovs - ofctl - O
        # OpenFlow13
        # add - group
        # br0
        # group_id = 111, type = all, bucket = output:2


        os.system(group_command)
        return group_id



    def push_match_per_in_port_destination_instruct_group_flow(self, bridge_dict, table_id, group_id, vlan_id,priority,in_port=None):

        if in_port is None:

            flow_rule = 'ovs-ofctl -O OpenFlow13 add-flow ' + ' ' + \
                    'tcp:' + bridge_dict['switch_IP'] + ':' + bridge_dict['of_port'] + ' ' + \
                    'table=' + str(table_id) + ',' + \
                    'priority=' + str(priority) + ',' + \
                    'vlan_vid='+ str(vlan_id) + ',' + \
                    'actions=group:' + str(group_id)
        else:

            flow_rule = 'ovs-ofctl -O OpenFlow13 add-flow ' + ' ' + \
                        'tcp:' + bridge_dict['switch_IP'] + ':' + bridge_dict['of_port'] + ' ' + \
                        'in_port=' + str(in_port.split('/')[2]) + ',' + \
                        'table=' + str(table_id) + ',' + \
                        'priority=' + str(priority) + ',' + \
                        'vlan_vid=' + str(vlan_id) + ',' + \
                        'actions=group:' + str(group_id)



        # TODO: Push a flow rule to the table_id at bridge_dict
        # Match on vlan_id
        # The only action is the group action defined by group_id

        # flow["match"] = flow_match.generate_match_json(self.network_graph.controller, flow["match"])
        # action_list = [{"type": "GROUP", "group_id": group_id}]
        # self.populate_flow_action_instruction(flow, action_list, apply_immediately)

        os.system(flow_rule)

