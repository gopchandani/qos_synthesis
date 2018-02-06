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

    def push_flow(self, bridge_dict, in_port, dst_mac, out_port, q_id):

        push_flow_cmd = "ovs-ofctl add-flow " + \
                       "tcp:" + bridge_dict["switch_IP"] + ":" + bridge_dict["of_port"] + " " \
                       "in_port=" + str(in_port.split('/')[2]) +  \
                       ",dl_dst=" + dst_mac + \
                        ",vlan_vid=0x1000/0x1000" + "," + \
                        "actions=strip_vlan," + "output:" + str(out_port.split('/')[2])
                        #"set_queue:" + str(q_id) + ","\


        os.system(push_flow_cmd)
        time.sleep(1)

    def push_queue(self, bridge_dict, port, min_rate, max_rate):
        self.queue_id_cntr_per_br[bridge_dict["bridge_name"]] +=  1
        min_rate_str = str(min_rate)
        max_rate_str = str(max_rate)

        queue_cmd = "ovs-vsctl " + \
                    "--db=tcp:" + bridge_dict["switch_IP"] + ":6640 -- " + \
                    "set Port " + port + " qos=@newqos -- " + \
                    "--id=@newqos create qos type=linux-htb other-config:max-rate=" + max_rate_str + \
                    " queues=" + str(self.queue_id_cntr_per_br[bridge_dict["bridge_name"]]) + \
                    "=@q" + str(self.queue_id_cntr_per_br[bridge_dict["bridge_name"]]) + \
                    " -- " +\
                    "--id=@q" + str(self.queue_id_cntr_per_br[bridge_dict["bridge_name"]]) + \
                    " create Queue other-config:min-rate=" + min_rate_str + \
                    " other-config:max-rate=" + max_rate_str

        os.system(queue_cmd)
        time.sleep(1)

        return self.queue_id_cntr_per_br[bridge_dict["bridge_name"]]

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

    def push_fast_failover_group_set_vlan_action(self, bridge_dict, intent_list, set_vlan_tags):
        self.group_id_cntr += 1
        group_id = self.group_id_cntr

        group_command = 'ovs-ofctl -O OpenFlow13 add-group' + ' ' \
                        'tcp:' + bridge_dict['switch_IP'] + ':' + bridge_dict['of_port'] + ' ' + \
                        'group_id=' + str(group_id) + ',' + \
                        'type=fast_failover' + ',' + \
                        'bucket=watch_port:' + intent_list[0].out_port.split('/')[2] + ',' \
                        'actions=mod_vlan_vid:' + str(set_vlan_tags[0]) + ',output:' + \
                        intent_list[0].out_port.split('/')[2] + ',' + \
                        'bucket=watch_port:' + intent_list[1].out_port.split('/')[2] + ',' \
                        'actions=mod_vlan_vid:' + str(set_vlan_tags[1]) + ',output:' + \
                        intent_list[1].out_port.split('/')[2]


        #TODO: Push a fast failover group where each bucket correspond to the intent in the intent_list
        # Each bucket has two actions: It sets the vlan_id to the corresponding index in set_vlan_tags
        # And sends the packet out to the out_port in the intent
        # The watch port for a bucket is same as the out_port of the intent

        # group["type"] = "FF"
        # bucket_list = []
        # for i in range(len(intent_list)):
        #
        #     intent = intent_list[i]
        #
        #     out_port, watch_port = self.get_out_and_watch_port(intent)
        #     bucket = {}
        #     bucket["actions"] = [{"type": "SET_FIELD", "field": "vlan_vid", "value": set_vlan_tags[i] + 0x1000},
        #                          {"type": "OUTPUT", "port": out_port}]
        #
        #     bucket["watch_port"] = watch_port
        #     bucket["watch_group"] = 4294967295
        #     bucket_list.append(bucket)
        #
        # group["buckets"] = bucket_list
        # group_id = group["group_id"]

        os.system(group_command)
        return group_id

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

