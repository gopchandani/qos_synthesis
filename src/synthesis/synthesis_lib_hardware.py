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
        self.queue_id_cntr = 1

        self.synthesized_primary_paths = defaultdict(defaultdict)
        self.synthesized_failover_paths = defaultdict(defaultdict)        

    def push_flow(self):
        pass

    def push_queue(self, sw, port, min_rate, max_rate):
        self.queue_id_cntr_per_sw[sw] = self.queue_id_cntr_per_sw[sw] + 1
        # self.queue_id_cntr = self.queue_id_cntr + 1
        min_rate_str = str(min_rate)
        max_rate_str = str(max_rate)
        # sw_port_str = sw + "-" + "eth" + str(port)
        sw_port_str = "ge-1/1/" + str(port)

        queue_cmd = "ovs-vsctl " + \
                    "--db=tcp:" + ip_map[sw] + ":6640 -- " + \
                    "set Port " + sw_port_str + " qos=@newqos -- " + \
                    "--id=@newqos create qos type=linux-htb other-config:max-rate=" + max_rate_str + \
                    " queues=" + str(self.queue_id_cntr_per_sw[sw]) + \
                    "=@q" + str(self.queue_id_cntr_per_sw[sw]) + \
                    " -- " +\
                    "--id=@q" + str(self.queue_id_cntr_per_sw[sw]) + \
                    " create Queue other-config:min-rate=" + min_rate_str + \
                    " other-config:max-rate=" + max_rate_str

        os.system(queue_cmd)
        time.sleep(1)

        return self.queue_id_cntr_per_sw[sw]
