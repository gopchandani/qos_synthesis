import networkx as nx
from synthesis.synthesis_lib_hardware import SynthesisLibHardware


class SynthesizeSimpleBackupFlows(object):

    def __init__(self, params):

        self.params = params
        self.synthesis_lib =  SynthesisLibHardware(params["nc"])

    # TODO: Transform paths in the equivalent queues, groups and rule objects in the flow descriptions
    def generate_flows_queues_groups(self, path, queue_priority, flow_rule_priority):
        rules = []
        queues = []
        groups = []

        things = {
            "rules"  : rules,
            "queues" : queues
        }

        for i in range(1, (len(path)-1)):
            cur_node = path[i]
            next_node = path[i+1]

            queue_dict = {
                "sw_name" : cur_node,
                "out_port" :self.params["nc"].get_link_dict(cur_node, next_node)["node1_port"] ,
                "min_rate" : int(1e9),
                "max_rate" : int(1e9),
                "queue_priority" : queue_priority,
            }

            queues.append(queue_dict)

            rule_dict = {
                "sw_name" : cur_node,
                "flow_type" : "normal",
                "out_port" : self.params["nc"].get_link_dict(cur_node,next_node)["node1_port"],
                "src_ip" : self.params["nc"].get_host_dict(path[0])["host_ip"],
                "dst_ip" : self.params["nc"].get_host_dict(path[len(path)-1])["host_ip"],
                "queue_num" : queue_priority,
                "flow_rule_priority" : flow_rule_priority
            }
            rules.append(rule_dict)

        return things


    def compute_switch_configurations(self):

        # Use Dijkstra to generate paths.
        # for src_host_dict in self.params["nc"].host_dict_iter():
        #     for target_host_dict in self.params["nc"].host_dict_iter():
        #
        #         if src_host_dict["host_name"] == target_host_dict["host_name"]:
        #             continue

        for f in self.params["flows"]:

            src_host_dict = self.params["nc"].get_host_dict(f["client"])
            target_host_dict = self.params["nc"].get_host_dict(f["server"])

            path = nx.shortest_path(self.params["nc"].graph,
                                    source=src_host_dict["host_name"],
                                    target=target_host_dict["host_name"])

            print(path)
            if f["type"] == "ptp":
                flow_rule_priority = 2
            elif f["type"] == "data":
                flow_rule_priority = 1
            else:
                flow_rule_priority = 0

            things = self.generate_flows_queues_groups(path, f["priority"],flow_rule_priority)
            f["rules"] = things["rules"]
            f["queues"] = things["queues"]

    def trigger(self):

        for f in self.params["flows"]:

            for q in f["queues"]:
                self.synthesis_lib.push_queue(self.params["nc"].get_switch_dict(q["sw_name"]),
                                              q["out_port"],
                                              q["min_rate"],
                                              q["max_rate"],
                                              q["queue_priority"])

            # for g in f["groups"]:
            #     self.synthesis_lib.push_group(self.params["nc"].get_switch_dict(g["sw_name"]),
            #                                   g["group_id"],
            #                                   g["group_type"],
            #                                   g["buckets"])

            for r in f["rules"]:
                if r["flow_type"] == "normal":

                    self.synthesis_lib.push_flow_rule(self.params["nc"].get_switch_dict(r["sw_name"]),
                                                                                    r["src_ip"],
                                                                                    r["dst_ip"],
                                                                                    f["port"],
                                                                                    r["out_port"],
                                                                                    r["flow_rule_priority"],
                                                                                    r["queue_num"])

                elif r["flow_type"] == "group":

                    self.synthesis_lib.push_flow_rule_group(self.params["nc"].get_switch_dict(r["sw_name"]),
                                                                                    r["group_id"],
                                                                                    r["src_ip"],
                                                                                    r["dst_ip"],
                                                                                    f["port"],
                                                                                    r["flow_rule_priority"],
                                                                                    )
