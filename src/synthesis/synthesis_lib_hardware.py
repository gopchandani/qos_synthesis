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

    def push_flow(self, bridge_dict, port, src_mac, dst_mac, q_id):
        pass

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
