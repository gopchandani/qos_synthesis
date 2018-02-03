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
                        ",actions=" + "output:" + str(out_port.split('/')[2])
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

    def push_table_miss_goto_next_table_flow(self, bridge_dict, table_id):

        dst_table_id = table_id + 1

        flow_rule = "ovs-ofctl" + " " + \
                    "add-flow " + "tcp:"+ bridge_dict["switch_IP"] + ":" + \
                    bridge_dict["of_port"] + " " + \
                    "table=" + str(table_id)+ "," + "actions=goto_table:" + str(dst_table_id)

        os.system(flow_rule)

    def push_flow_rule_match_dst_mac_action_outport(self,bridge_dict, dst_mac,out_port, table_id):

        flow_rule = "ovs-ofctl" + " " + \
                    "add-flow " + "tcp:"+ bridge_dict["switch_IP"] + ":" + bridge_dict["of_port"] + ": " + \
                    "table=" + str(table_id) + "," + \
                    "dl_dst=" + dst_mac + "," + \
                    "actions=output:" + str(out_port.split('/')[2])

        os.system(flow_rule)
