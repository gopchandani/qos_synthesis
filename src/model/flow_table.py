__author__ = 'Rakesh Kumar'


from match import Match
from instruction_set import InstructionSet


class Flow:

    def __hash__(self):
        return hash(str(self.sw.node_id) + str(self.table_id) + str(id(self)))

    def __init__(self, sw, flow_table, flow_json):

        self.sw = sw
        self.flow_table = flow_table
        self.flow_json = flow_json
        self.network_graph = sw.network_graph
        self.network_graph.total_flow_rules += 1

        self.written_actions = []
        self.applied_actions = []
        self.go_to_table = None

        self.instruction_set = None

        if self.sw.network_graph.controller == "ryu":
            self.table_id = self.flow_json["table_id"]
            self.priority = int(self.flow_json["priority"])
            self.match = Match(match_json=self.flow_json["match"], controller="ryu", flow=self)
            self.instruction_set = InstructionSet(self.sw, self, self.flow_json["instructions"])

        elif self.sw.network_graph.controller == "ryu_old":
            self.table_id = self.flow_json["table_id"]
            self.priority = int(self.flow_json["priority"])
            self.match = Match(match_json=self.flow_json["match"], controller="ryu", flow=self)
            self.instruction_set = InstructionSet(self.sw, self, self.flow_json["actions"])
        else:
            raise NotImplemented


class FlowTable:
    def __init__(self, sw, table_id, flow_list):

        self.sw = sw
        self.network_graph = sw.network_graph
        self.table_id = table_id
        self.flows = []

        for f in flow_list:
            f = Flow(sw, self, f)
            self.flows.append(f)

        #  Sort the flows list by priority
        self.flows = sorted(self.flows, key=lambda flow: flow.priority, reverse=True)
