__author__ = 'Rakesh Kumar'

import pprint
import time
import httplib2
import json
import os
import sys

from collections import defaultdict


class SynthesisLib(object):

    def __init__(self, controller_host, controller_port, network_graph):

        self.network_graph = network_graph

        self.controller_host = controller_host
        self.controller_port = controller_port

        self.group_id_cntr = 0
        self.flow_id_cntr = 0
        self.queue_id_cntr = 1

        self.queue_id_cntr_per_sw = {
            "s2347862419956695048": 0,
            "s2347862419956695105": 0
        }

        self.h = httplib2.Http(".cache")
        self.h.add_credentials('admin', 'admin')

        # Cleanup all Queue/QoS records from OVSDB
        os.system("sudo ovs-vsctl --db=tcp:192.168.1.103:6640 clear Port ge-1/1/43")
        os.system("sudo ovs-vsctl --db=tcp:192.168.1.103:6640 clear Port ge-1/1/45")
        os.system("sudo ovs-vsctl --db=tcp:192.168.1.103:6640 clear Port ge-1/1/47")
        os.system("sudo ovs-vsctl --db=tcp:192.168.1.103:6640 -- --all destroy QoS")
        os.system("sudo ovs-vsctl --db=tcp:192.168.1.103:6640 -- --all destroy Queue")

        os.system("sudo ovs-vsctl --db=tcp:192.168.1.101:6640 clear Port ge-1/1/43")
        os.system("sudo ovs-vsctl --db=tcp:192.168.1.101:6640 clear Port ge-1/1/45")
        os.system("sudo ovs-vsctl --db=tcp:192.168.1.101:6640 clear Port ge-1/1/47")
        os.system("sudo ovs-vsctl --db=tcp:192.168.1.101:6640 -- --all destroy QoS")
        os.system("sudo ovs-vsctl --db=tcp:192.168.1.101:6640 -- --all destroy Queue")

        self.synthesized_primary_paths = defaultdict(defaultdict)
        self.synthesized_failover_paths = defaultdict(defaultdict)        

    def record_primary_path(self, src_host, dst_host, switch_port_tuple_list):

        port_path = []
        
        for sw_name, ingress_port_number, egress_port_number in switch_port_tuple_list:
            port_path.append(sw_name + ":ingress" + str(ingress_port_number))
            port_path.append(sw_name + ":egress" + str(egress_port_number))

        self.synthesized_primary_paths[src_host.node_id][dst_host.node_id] = port_path
        
    def record_failover_path(self, src_host, dst_host, e, switch_port_tuple_list):

        port_path = []
        
        if src_host.node_id not in self.synthesized_failover_paths:
            if dst_host.node_id not in self.synthesized_failover_paths[src_host.node_id]:
                self.synthesized_failover_paths[src_host.node_id][dst_host.node_id] = defaultdict(defaultdict)
        else:
            if dst_host.node_id not in self.synthesized_failover_paths[src_host.node_id]:
                self.synthesized_failover_paths[src_host.node_id][dst_host.node_id] = defaultdict(defaultdict)

        for sw_name, ingress_port_number, egress_port_number in switch_port_tuple_list:
            port_path.append(sw_name + ":ingress" + str(ingress_port_number))
            port_path.append(sw_name + ":egress" + str(egress_port_number))

        self.synthesized_failover_paths[src_host.node_id][dst_host.node_id][e[0]][e[1]] = port_path

    def save_synthesized_paths(self, conf_path):
        with open(conf_path + "synthesized_primary_paths.json", "w") as outfile:
            json.dump(self.synthesized_primary_paths, outfile)

        with open(conf_path + "synthesized_failover_paths.json", "w") as outfile:
            json.dump(self.synthesized_failover_paths, outfile)

    def push_queue(self, sw, port, min_rate, max_rate):
        self.queue_id_cntr_per_sw[sw] = self.queue_id_cntr_per_sw[sw] + 1
        # self.queue_id_cntr = self.queue_id_cntr + 1
        min_rate_str = str(min_rate)
        max_rate_str = str(max_rate)
        # sw_port_str = sw + "-" + "eth" + str(port)
        sw_port_str = "ge-1/1/" + str(port)

        ip_map = {
            "s2347862419956695048": "192.168.1.103",
            "s2347862419956695105": "192.168.1.101"
        }

        queue_cmd = "ovs-vsctl --db=tcp:" + ip_map[sw] + ":6640 -- set Port " + sw_port_str + " qos=@newqos -- " + \
              "--id=@newqos create QoS type=linux-htb other-config:max-rate=" + "1000000000" + \
                    " queues=" + str(self.queue_id_cntr) + "=@q" + str(self.queue_id_cntr_per_sw[sw]) + " -- " +\
              "--id=@q" + str(self.queue_id_cntr_per_sw[sw]) + " create Queue other-config:min-rate=" + min_rate_str + \
              " other-config:max-rate=" + max_rate_str

        print queue_cmd

        # queue_cmd = "sudo ovs-vsctl --db=tcp:192.168.1.103:6640 -- set Port " + sw_port_str + " qos=@newqos -- " + \
        #             "--id=@newqos create QoS type=linux-htb other-config:max-rate=" + "1000000000" + \
        #             " queues=" + str(self.queue_id_cntr) + "=@q" + str(self.queue_id_cntr) + " -- " + \
        #             "--id=@q" + str(self.queue_id_cntr) + " create Queue other-config:min-rate=" + min_rate_str + \
        #             " other-config:max-rate=" + max_rate_str

        os.system(queue_cmd)
        time.sleep(1)

        return self.queue_id_cntr_per_sw[sw]

    def sel_get_node_id(self, switch):
       # for node in ConfigTree.nodesHttpAccess(self.sel_session).read_collection():
         for node in ConfigTree.NodesEntityAccess(self.sel_session).read_collection():
            if node.linked_key == "OpenFlow:{}".format(switch[1:]):
                return node.id

    def push_change(self, url, pushed_content):

        time.sleep(0.2)

        if self.network_graph.controller == "ryu" or self.network_graph.controller == "ryu_old":
            #import pdb; pdb.set_trace()
            resp, content = self.h.request(url, "POST",
                                           headers={'Content-Type': 'application/json; charset=UTF-8'},
                                           body=json.dumps(pushed_content))

        elif self.network_graph.controller == "sel":
            raise NotImplementedError
        #resp = {"status": "200"}
        #pprint.pprint(pushed_content)

        if resp["status"] == "200":
            print "Pushed Successfully:", pushed_content.keys()[0]
            #print resp["status"]
        else:
            print "Problem Pushing:", pushed_content.keys()[0]
            print "resp:", resp, "content:", content
            pprint.pprint(pushed_content)

    def create_ryu_flow_url(self):
        return "http://192.168.1.102:8080/stats/flowentry/add"

    def create_ryu_group_url(self):
        return "http://192.168.1.102:8080/stats/groupentry/add"

    def push_flow(self, sw, flow):

        url = None
        if self.network_graph.controller == "ryu" or self.network_graph.controller == "ryu_old":
            url = self.create_ryu_flow_url()

        elif self.network_graph.controller == "sel":
            raise NotImplemented

        self.push_change(url, flow)

    def push_group(self, sw, group):

        url = None
        if self.network_graph.controller == "ryu":
            url = self.create_ryu_group_url()

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        self.push_change(url, group)

    def create_base_flow(self, sw, table_id, priority):

        self.flow_id_cntr +=  1
        flow = dict()

        if self.network_graph.controller == "ryu":

            flow["dpid"] = sw[1:]
            flow["cookie"] = self.flow_id_cntr
            flow["cookie_mask"] = 1
            flow["table_id"] = table_id
            flow["idle_timeout"] = 0
            flow["hard_timeout"] = 0
            flow["priority"] = priority + 10
            flow["flags"] = 1
            flow["match"] = {}
            flow["instructions"] = []

        elif self.network_graph.controller == "ryu_old":

            flow["dpid"] = sw[1:]
            flow["cookie"] = self.flow_id_cntr
            flow["cookie_mask"] = 1
            flow["table_id"] = table_id
            flow["idle_timeout"] = 0
            flow["hard_timeout"] = 0
            flow["priority"] = priority + 100
            flow["flags"] = 1
            flow["match"] = {}
            flow["instructions"] = []

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        return flow

    def create_base_group(self, sw):

        group = dict()
        self.group_id_cntr += 1

        if self.network_graph.controller == "ryu":

            group["dpid"] = sw[1:]
            group["type"] = ""
            group["group_id"] = self.group_id_cntr
            group["buckets"] = []

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        return group

    def populate_flow_action_instruction(self, flow, action_list, apply_immediately):

        if self.network_graph.controller == "ryu":

            if not action_list:
                flow["instructions"] = []
            else:

                if apply_immediately:
                    flow["instructions"] = [{"type": "APPLY_ACTIONS",
                                             "actions": action_list}]
                else:
                    flow["instructions"] = [{"type": "WRITE_ACTIONS",
                                             "actions": action_list}]

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        return flow


    def push_table_miss_goto_next_table_flow(self, sw, table_id):

        # Create a lowest possible flow
        flow = self.create_base_flow(sw, table_id, 0)

        #Compile instruction
        #  Assert that packet be sent to table with this table_id + 1

        if self.network_graph.controller == "ryu":
            flow["instructions"] = [{"type": "GOTO_TABLE",  "table_id": str(table_id + 1)}]

        if self.network_graph.controller == "ryu_old":
            flow["actions"] = [{"type": "GOTO_TABLE",  "table_id": table_id + 1}]

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        self.push_flow(sw, flow)

    def push_flow_with_group_and_set_vlan(self, sw, flow_match, table_id, vlan_id, group_id, priority, apply_immediately):

        flow = self.create_base_flow(sw, table_id, priority)

        if self.network_graph.controller == "ryu":
            flow["match"] = flow_match.generate_match_json(self.network_graph.controller, flow["match"],
                                                           has_vlan_tag_check=True)

            action_list = [{"type": "SET_FIELD", "field": "vlan_vid", "value": vlan_id + 0x1000},
                           {"type": "GROUP", "group_id": group_id}]

            self.populate_flow_action_instruction(flow, action_list, apply_immediately)

        elif self.network_graph.controller == "sel":
            raise NotImplemented

        self.push_flow(sw, flow)

        return flow

    def push_match_per_in_port_destination_instruct_flow(self, sw, table_id, priority, flow_match, output_port, apply_immediately):

        flow = self.create_base_flow(sw, table_id, priority)

        if self.network_graph.controller == "ryu":
            flow["match"] = flow_match.generate_match_json(self.network_graph.controller, flow["match"])
            action_list = [{"type": "GROUP", "group_id": group_id}]
            self.populate_flow_action_instruction(flow, action_list, apply_immediately)

        elif self.network_graph.controller == "ryu_old":
            flow["match"] = flow_match.generate_match_json(self.network_graph.controller, flow["match"])
            action_list = [{"type": "OUTPUT", "port": output_port}]
            flow["actions"] = action_list

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        self.push_flow(sw, flow)

        return flow

    def push_match_per_in_port_destination_instruct_group_flow(self, sw, table_id, group_id, priority,
                                                                flow_match, apply_immediately):

        flow = self.create_base_flow(sw, table_id, priority)

        if self.network_graph.controller == "ryu":
            flow["match"] = flow_match.generate_match_json(self.network_graph.controller, flow["match"])
            action_list = [{"type": "GROUP", "group_id": group_id}]
            self.populate_flow_action_instruction(flow, action_list, apply_immediately)

        elif self.network_graph.controller == "ryu_old":
            flow["match"] = flow_match.generate_match_json(self.network_graph.controller, flow["match"])
            action_list = [{"type": "GROUP", "group_id": group_id}]
            flow["actions"] = action_list

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        self.push_flow(sw, flow)

        return flow

    def get_out_and_watch_port(self, intent):
        out_port = None
        watch_port = None

        if intent.in_port == intent.out_port:
            out_port = self.network_graph.OFPP_IN
            watch_port = intent.out_port
        else:
            out_port = intent.out_port
            watch_port = intent.out_port

        return out_port, watch_port

    def push_fast_failover_group(self, sw, primary_intent, failover_intent):

        group = self.create_base_group(sw)
        group_id = None

        if self.network_graph.controller == "ryu":

            group["type"] = "FF"

            bucket_primary = {}
            bucket_failover = {}

            out_port, watch_port = self.get_out_and_watch_port(primary_intent)
            bucket_primary["actions"] = [{"type": "OUTPUT", "port": out_port}]
            bucket_primary["watch_port"] = watch_port
            bucket_primary["watch_group"] = 4294967295

            out_port, watch_port = self.get_out_and_watch_port(failover_intent)
            bucket_failover["actions"] = [{"type": "OUTPUT", "port": out_port}]
            bucket_failover["watch_port"] = watch_port
            bucket_primary["watch_group"] = 4294967295

            group["buckets"] = [bucket_primary, bucket_failover]
            group_id = group["group_id"]

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        self.push_group(sw, group)

        return group_id

    def push_fast_failover_group_set_vlan_action(self, sw, intent_list, set_vlan_tags):

        group = self.create_base_group(sw)
        group_id = None

        if self.network_graph.controller == "ryu":
            group["type"] = "FF"
            bucket_list = []
            for i in range(len(intent_list)):

                intent = intent_list[i]

                out_port, watch_port = self.get_out_and_watch_port(intent)
                bucket = {}
                bucket["actions"] = [{"type": "SET_FIELD", "field": "vlan_vid", "value": set_vlan_tags[i] + 0x1000},
                                     {"type": "OUTPUT", "port": out_port}]

                bucket["watch_port"] = watch_port
                bucket["watch_group"] = 4294967295
                bucket_list.append(bucket)

            group["buckets"] = bucket_list
            group_id = group["group_id"]

        elif self.network_graph.controller == "sel":
            raise NotImplemented

        self.push_group(sw, group)

        return group_id

    def push_select_all_group(self, sw, intent_list):

        if not intent_list:
            raise Exception("Need to have either one or two forwarding intents")

        group = self.create_base_group(sw)
        group_id = None

        if self.network_graph.controller == "ryu":
            group["type"] = "ALL"
            group["buckets"] = []

            for intent in intent_list:
                this_bucket = {}

                output_action = {"type": "OUTPUT", "port": intent.out_port}

                if intent.min_rate and intent.max_rate:
                    q_id = self.push_queue(sw, intent.out_port, intent.min_rate, intent.max_rate)
                    enqueue_action = {"type": "SET_QUEUE", "queue_id": q_id, "port": intent.out_port}
                    action_list = [enqueue_action, output_action]
                    this_bucket["actions"] = [output_action]
                else:
                    out_port, watch_port = self.get_out_and_watch_port(intent)
                    action_list = [output_action]

                this_bucket["actions"] = action_list
                group["buckets"].append(this_bucket)

            group_id = group["group_id"]

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        self.push_group(sw, group)

        return group_id

    def push_select_all_group_set_vlan_action(self, sw, intent_list, modified_tag):

        if not intent_list:
            raise Exception("Need to have either one or two forwarding intents")

        group = self.create_base_group(sw)
        group_id = None

        if self.network_graph.controller == "ryu":
            group["type"] = "ALL"
            group["buckets"] = []

            for intent in intent_list:
                this_bucket = {}

                set_vlan_action = {"type": "SET_FIELD", "field": "vlan_vid", "value": modified_tag + 0x1000}
                output_action = {"type": "OUTPUT", "port": intent.out_port}

                action_list = [set_vlan_action, output_action]

                this_bucket["actions"] = action_list
                group["buckets"].append(this_bucket)

            group_id = group["group_id"]

        elif self.network_graph.controller == "sel":
            raise NotImplemented

        self.push_group(sw, group)

        return group_id

    def push_destination_host_mac_intent_flow(self, sw, mac_intent, table_id, priority):

        flow = self.create_base_flow(sw, table_id, priority)

        output_action = None

        if self.network_graph.controller == "ryu":
            flow["match"] = mac_intent.flow_match.generate_match_json(self.network_graph.controller, flow["match"])
            output_action = {"type": "OUTPUT", "port": mac_intent.out_port}

            action_list = [output_action]

            self.populate_flow_action_instruction(flow, action_list, mac_intent.apply_immediately)
            self.push_flow(sw, flow)

        elif self.network_graph.controller == "ryu_old":
            flow["match"] = mac_intent.flow_match.generate_match_json(self.network_graph.controller, flow["match"])
            output_action = {"type": "OUTPUT", "port": mac_intent.out_port}

            flow["actions"] = [output_action]

            self.push_flow(sw, flow)

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        return flow

    def push_destination_host_mac_intent_flow_with_qos(self, switch_id, mac_intent, table_id, priority):

        flow = self.create_base_flow(switch_id, table_id, priority)

        if  self.network_graph.controller == "ryu":
            flow["match"] = mac_intent.flow_match.generate_match_json(self.network_graph.controller, flow["match"])
            output_action = {"type": "OUTPUT", "port": mac_intent.out_port}

            q_id = self.push_queue(switch_id, mac_intent.out_port, mac_intent.min_rate, mac_intent.max_rate)
            enqueue_action = {"type": "SET_QUEUE", "queue_id": q_id, "port": mac_intent.out_port}
            action_list = [enqueue_action, output_action]

            self.populate_flow_action_instruction(flow, action_list, mac_intent.apply_immediately)
            self.push_flow(switch_id, flow)

        if self.network_graph.controller == "ryu_old":
            flow["match"] = mac_intent.flow_match.generate_match_json(self.network_graph.controller, flow["match"])
            output_action = {"type": "OUTPUT", "port": mac_intent.out_port}

            q_id = self.push_queue(switch_id, mac_intent.out_port, mac_intent.min_rate, mac_intent.max_rate)
            enqueue_action = {"type": "SET_QUEUE", "queue_id": q_id, "port": mac_intent.out_port}
            action_list = [enqueue_action, output_action]
            flow["actions"] = action_list

            # self.populate_flow_action_instruction(flow, action_list, mac_intent.apply_immediately)
            self.push_flow(switch_id, flow)

        return flow

    def push_destination_host_mac_vlan_intent_flow(self, sw, mac_intent, table_id, priority):

        flow = self.create_base_flow(sw, table_id, priority)

        pop_vlan_action = None
        output_action = None

        if self.network_graph.controller == "ryu":
            flow["match"] = mac_intent.flow_match.generate_match_json(self.network_graph.controller, flow["match"],
                                                                      has_vlan_tag_check=True)
            pop_vlan_action = {"type": "POP_VLAN"}
            output_action = {"type": "OUTPUT", "port": mac_intent.out_port}

        elif self.network_graph.controller == "ryu_old":
            flow["match"] = mac_intent.flow_match.generate_match_json(self.network_graph.controller, flow["match"],
                                                                      has_vlan_tag_check=True)
            pop_vlan_action = {"type": "POP_VLAN"}
            output_action = {"type": "OUTPUT", "port": mac_intent.out_port}

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        action_list = None
        if mac_intent.min_rate and mac_intent.max_rate:
            q_id = self.push_queue(sw, mac_intent.out_port, mac_intent.min_rate, mac_intent.max_rate)
            if self.network_graph.controller == "ryu":
                enqueue_action = {"type": "SET_QUEUE", "queue_id": q_id, "port": mac_intent.out_port}
                action_list = [pop_vlan_action, enqueue_action, output_action]
        else:
            action_list = [pop_vlan_action, output_action]

        if self.network_graph.controller == "ryu_old":
            flow["actions"] = action_list
        else:
            self.populate_flow_action_instruction(flow, action_list, mac_intent.apply_immediately)

        self.push_flow(sw, flow)

        return flow

    def push_destination_host_mac_intents(self, sw, mac_intents, mac_forwarding_table_id, pop_vlan=True):

        if mac_intents:

            if len(mac_intents) > 1:
                print "There are more than one mac intents for a single dst, will install only one"

            if pop_vlan:
                self.push_destination_host_mac_vlan_intent_flow(sw,
                                                                mac_intents[0],
                                                                mac_forwarding_table_id,
                                                                100)

            self.push_destination_host_mac_intent_flow(sw, mac_intents[0], mac_forwarding_table_id, 10)

    def push_vlan_tagged_table_jump_rule(self, sw, flow_match, src_table, dst_table):
        flow = self.create_base_flow(sw, src_table, 1)

        if self.network_graph.controller == "ryu":
            flow["match"] = flow_match.generate_match_json(self.network_graph.controller,
                                                           flow["match"],
                                                           has_vlan_tag_check=True)

            flow["instructions"] = [{"type": "GOTO_TABLE",  "table_id": str(dst_table)}]

        elif self.network_graph.controller == "sel":
            raise NotImplemented

        self.push_flow(sw, flow)

    def push_flow_vlan_tag(self, sw, flow_match, vlan_tag_push_rules_table_id, apply_immediately):

        flow = self.create_base_flow(sw, vlan_tag_push_rules_table_id, 1)

        # Compile instructions
        if self.network_graph.controller == "ryu":

            # Compile match
            flow["match"] = flow_match.generate_match_json(self.network_graph.controller, flow["match"])

            action_list = [{"type": "PUSH_VLAN", "ethertype": 0x8100}]

            self.populate_flow_action_instruction(flow, action_list, apply_immediately)

            flow["instructions"].append({"type": "GOTO_TABLE", "table_id": str(vlan_tag_push_rules_table_id + 1)})

        elif self.network_graph.controller == "sel":
            raise NotImplemented

        self.push_flow(sw, flow)

    def push_vlan_push_intents(self, sw, push_vlan_intents, vlan_tag_push_rules_table_id):

        for push_vlan_intent in push_vlan_intents:
            flow = self.create_base_flow(sw, vlan_tag_push_rules_table_id, 1)

            # Compile instructions
            if self.network_graph.controller == "ryu":

                # Compile match
                flow["match"] = push_vlan_intent.flow_match.generate_match_json(self.network_graph.controller,
                                                                                flow["match"])

                action_list = [{"type": "PUSH_VLAN", "ethertype": 0x8100},
                               {"type": "SET_FIELD", "field": "vlan_vid", "value": push_vlan_intent.required_vlan_id + 0x1000}]

                self.populate_flow_action_instruction(flow, action_list, push_vlan_intent.apply_immediately)

                flow["instructions"].append({"type": "GOTO_TABLE", "table_id": str(vlan_tag_push_rules_table_id + 1)})

            if self.network_graph.controller == "ryu_old":

                # Compile match
                flow["match"] = push_vlan_intent.flow_match.generate_match_json(self.network_graph.controller,
                                                                                flow["match"])

                action_list = [{"type": "PUSH_VLAN", "ethertype": 0x8100},
                               {"type": "SET_FIELD", "field": "vlan_vid", "value": push_vlan_intent.required_vlan_id + 0x1000},
                               {"type": "GOTO_TABLE", "table_id": vlan_tag_push_rules_table_id + 1}]

                flow["actions"] = action_list

            elif self.network_graph.controller == "sel":
                raise NotImplementedError

            self.push_flow(sw, flow)

    def push_vlan_push_intents_2(self, sw, push_vlan_intent, vlan_tag_push_rules_table_id, group_id, apply_immediately):

        flow = self.create_base_flow(sw, vlan_tag_push_rules_table_id, 1)

        # Compile instructions
        if self.network_graph.controller == "ryu":

            # Compile match
            flow["match"] = push_vlan_intent.flow_match.generate_match_json(self.network_graph.controller,
                                                                            flow["match"])

            action_list = [{"type": "PUSH_VLAN", "ethertype": 0x8100},
                           {"type": "SET_FIELD", "field": "vlan_vid", "value": push_vlan_intent.required_vlan_id + 0x1000},
                           {"type": "GROUP", "group_id": group_id}]


            self.populate_flow_action_instruction(flow, action_list, push_vlan_intent.apply_immediately)

        elif self.network_graph.controller == "sel":
            raise NotImplementedError

        self.push_flow(sw, flow)
    
    def push_mac_acl_rules(self, sw, table_number, src_host, dst_host):

        # Get a vanilla flow with an empty action list so it can be dropped
        flow = self.create_base_flow(sw, table_number, 100)
        action_list = []

        # Make and push the flow
        if self.network_graph.controller == "ryu":
            flow["match"]["eth_src"] = src_host.mac_addr
            flow["match"]["eth_dst"] = dst_host.mac_addr
        else:
            raise NotImplemented

        self.populate_flow_action_instruction(flow, action_list, True)
        self.push_flow(sw, flow)
        
    def push_loop_preventing_drop_rules(self, sw, table_number):

        for h_id in self.network_graph.host_ids:

            # Get concerned only with hosts that are directly connected to this sw
            h_obj = self.network_graph.get_node_object(h_id)
            if h_obj.sw.node_id != sw:
                continue

            # Get a vanilla flow
            flow = self.create_base_flow(sw, table_number, 100)
            action_list = []

            # Compile match with in_port and destination mac address
            if self.network_graph.controller == "ryu":
                flow["match"]["in_port"] = h_obj.switch_port.port_number
                flow["match"]["eth_dst"] = h_obj.mac_addr

            elif self.network_graph.controller == "sel":
                raise NotImplemented

            # Make and push the flow
            self.populate_flow_action_instruction(flow, action_list, True)
            self.push_flow(sw, flow)

    def push_host_vlan_tagged_packets_drop_rules(self, sw, host_vlan_tagged_drop_table):

        for h_id in self.network_graph.host_ids:

            # Get concerned only with hosts that are directly connected to this sw
            h_obj = self.network_graph.get_node_object(h_id)
            if h_obj.sw.node_id != sw:
                continue

            # Get a vanilla flow
            flow = self.create_base_flow(sw, host_vlan_tagged_drop_table, 100)
            action_list = []

            #Compile match with in_port and destination mac address
            if self.network_graph.controller == "ryu":
                flow["match"]["in_port"] = h_obj.switch_port.port_number
                flow["match"]["vlan_vid"] = self.network_graph.graph.node[sw]["sw"].synthesis_tag

            elif self.network_graph.controller == "sel":
                raise NotImplementedError

            # Make and push the flow
            self.populate_flow_action_instruction(flow, action_list, True)
            self.push_flow(sw, flow)

