from synthesis.synthesis_lib_hardware import SynthesisLibHardware


class SynthesizeSimpleBackupFlows(object):

    def __init__(self, params):

        self.params = params
        self.synthesis_lib =  SynthesisLibHardware(params["nc"])

    #TODO:
    def compute_flow_rules_and_queues(self):
        pass

    def trigger(self):

        for f in self.params["flows"]:

            for q in f["queues"]:
                self.synthesis_lib.push_queue(self.params["nc"].get_switch_dict(q["sw_name"]),
                                              q["out_port"],
                                              q["min_rate"],
                                              q["max_rate"],
                                              q["queue_priority"])

            for g in f["groups"]:
                self.synthesis_lib.push_group(self.params["nc"].get_switch_dict(g["sw_name"]),
                                              g["group_id"],
                                              g["group_type"],
                                              g["buckets"])


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
