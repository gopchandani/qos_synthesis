__author__ = 'Rakesh Kumar'

from match import ryu_field_names_mapping
from collections import defaultdict


class Action:
    '''
     As per OF1.3 specification:

    Required Action: Output. The Output action forwards a packet to a specified OpenFlow port.
                            OpenFlow switches must support forwarding to physical ports, switch-defined logical ports
                            and the required reserved ports.

    Optional Action: Set-Queue. The set-queue action sets the queue id for a packet. When the packet is forwarded to
                            a port using the output action, the queue id determines which queue attached to this port
                            is used for scheduling and forwarding the packet. Forwarding behavior is dictated by the
                            configuration of the queue and is used to provide basic Quality-of-Service (QoS) support

    Required Action: Drop. There is no explicit action to represent drops. Instead, packets whose action sets have no
                            output actions should be dropped. This result could come from empty instruction sets or
                            empty action buckets in the processing pipeline, or after executing a Clear-Actions
                            instruction.

    Required Action: Group. Process the packet through the specified group. The exact interpretation depends on group
                            type.
    Optional Action: Push-Tag/Pop-Tag. Switches may support the ability to push/pop tags. To aid
                            integration with existing networks, we suggest that the ability to push/pop VLAN tags be
                            supported.
    '''

    def __init__(self, sw, action_json):

        self.action_json = action_json
        self.sw = sw
        self.action_type = None
        self.bucket = None
        self.instruction_type = None

        self.vuln_rank = 0

        # Captures what the action is doing.
        self.modified_field = None
        self.field_modified_to = None

        if self.sw.network_graph.controller == "ryu":
            self.parse_ryu_action_json()
        elif self.sw.network_graph.controller == "ryu_old":
            self.parse_ryu_action_json_old()
        else:
            raise NotImplemented

    def get_active_rank(self):

        prior_active_watch_ports = []
        if self.bucket:
            prior_active_watch_ports = self.bucket.prior_active_watch_ports()

        return len(prior_active_watch_ports)

    def parse_ryu_action_json_old(self):

        if self.action_json.startswith("OUTPUT"):
            self.action_type = "output"
            self.out_port = self.action_json.split(":")[1]
        else:
            raise NotImplemented

    def parse_ryu_action_json(self):

        if self.action_json["type"] == "OUTPUT":
            self.action_type = "output"
            self.out_port = self.action_json["port"]

        if self.action_json["type"] == "SET_FIELD":
            self.action_type = "set_field"

            self.modified_field = ryu_field_names_mapping[self.action_json["field"]]

            #TODO: Works fine for VLAN_ID mods, other fields may require special parsing here
            if self.action_json["field"] == "vlan_vid":
                self.field_modified_to = self.action_json["value"]
                self.field_modified_to = int(self.field_modified_to)
            else:
                raise NotImplemented

        if self.action_json["type"] == "GROUP":
            self.action_type = "group"
            self.group_id = self.action_json["group_id"]

        if self.action_json["type"] == "PUSH_VLAN":
            self.action_type = "push_vlan"

        if self.action_json["type"] == "POP_VLAN":
            self.action_type = "pop_vlan"

    def is_failover_action(self):
        return (self.bucket and self.bucket.group.group_type == self.sw.network_graph.GROUP_FF)


class ActionSet:

    '''
    As per OF1.3 specification:

    An action set is associated with each packet.
    An action set contains a maximum of one action of each type.
    The set-field actions are identified by their field types, therefore the action set contains a maximum of one
    set-field action for each field type (i.e. multiple fields can be set). When multiple actions of the same type are
    required, e.g. pushing multiple MPLS labels or popping multiple MPLS labels, the Apply-Actions instruction may be
    used.


    The actions in an action set are applied in the order specified below,
    regardless of the order that they were added to the set.
    If an action set contains a group action, the actions in the appropriate action bucket
    of the group are also applied in the order specified below. The switch may support arbitrary
    action execution order through the action list of the Apply-Actions instruction.

    1. copy TTL inwards: apply copy TTL inward actions to the packet
    2. pop: apply all tag pop actions to the packet
    3. push-MPLS: apply MPLS tag push action to the packet
    4. push-PBB: apply PBB tag push action to the packet
    5. push-VLAN: apply VLAN tag push action to the packet
    6. copy TTL outwards: apply copy TTL outwards action to the packet
    7. decrement TTL: apply decrement TTL action to the packet
    8. set: apply all set-field actions to the packet
    9. qos: apply all QoS actions, such as set queue to the packet
    10. group: if a group action is specified, apply the actions of the relevant group bucket(s) in the order specified by this list
    11. output: if no group action is specified, forward the packet on the port specified by the output action

    The output action in the action set is executed last. If both an output action and a group action are specified
    in an action set, the output action is ignored and the group action takes precedence.
    If no output action and no group action were specified in an action set, the packet is dropped.
    The execution of groups is recursive if the switch supports it; a group bucket may specify another group,
    in which case the execution of actions traverses all the groups specified by the group configuration.

    '''

    def __init__(self, sw):

        # network_graphling the ActionSet as a dictionary of lists, keyed by various actions.
        # These actions may be tucked away inside a group too and the type might be group

        self.action_dict = defaultdict(list)
        self.sw = sw

    def add_all_actions(self, action_list):

        for action in action_list:

            if action.action_type == "group":
                if action.group_id in self.sw.group_table.groups:
                    group_all_action_list =  self.sw.group_table.groups[action.group_id].get_action_list()
                    self.add_all_actions(group_all_action_list)
                else:
                    raise Exception("Odd that a group_id is not provided in a group action")
            else:
                self.action_dict[action.action_type].append(action)

    def remove_all_actions(self):
        self.action_dict.clear()

    def get_modified_fields_dict(self, flow_match_element):
        modified_fields_dict = {}

        # Capture the value before (in principle and after) the modification in a tuple
        for set_action in self.action_dict["set_field"]:
            value_tree = IntervalTree([Interval(set_action.field_modified_to, set_action.field_modified_to + 1)])
            modified_fields_dict[set_action.modified_field] = (flow_match_element, value_tree)

        if "push_vlan" in self.action_dict:
            value_tree = IntervalTree([Interval(1, 2)])
            modified_fields_dict["has_vlan_tag"] = (flow_match_element, value_tree)

        # A vlan tag popped means, the field does not matter anymore
        if "pop_vlan" in self.action_dict:
            value_tree = IntervalTree([Interval(0, 1)])
            modified_fields_dict["has_vlan_tag"] = (flow_match_element, value_tree)

        return modified_fields_dict

    def get_action_set_output_action_edges(self):

        port_graph_edges = []

        for output_action in self.action_dict["output"]:

            if int(output_action.out_port) == self.sw.network_graph.OFPP_CONTROLLER:
                continue

            if int(output_action.out_port) == self.sw.network_graph.OFPP_NORMAL:
                continue

            if output_action.is_failover_action():

                # If the output port is specified to be same as input port
                if int(self.sw.network_graph.OFPP_IN) == int(output_action.out_port):

                    # Consider all possible ports
                    for in_port in self.sw.ports:

                        # if they are currently up
                        if self.sw.ports[in_port].state != "up":
                            continue

                        # If they are not the watch port of actions that may have come before
                        # this action in a failover rule, because that port has failed already, no need to
                        # add an edge going there
                        if in_port in output_action.bucket.prior_failed_ports():
                            continue

                        port_graph_edges.append((str(in_port), output_action))

                else:
                    # Add an edge, only if the output_port is currently up
                    if self.sw.ports[output_action.out_port].state == "up":
                        port_graph_edges.append((str(output_action.out_port), output_action))

            else:
                # If the output port is specified to be same as input port
                if int(self.sw.network_graph.OFPP_IN) == int(output_action.out_port):

                    # Consider all possible ports
                    for in_port in self.sw.ports:
                        # if they are currently up
                        if self.sw.ports[in_port].state != "up":
                            continue
                        port_graph_edges.append((str(in_port), output_action))

                else:

                    # Add an edge, only if the output_port is currently up
                    if self.sw.ports[output_action.out_port].state == "up":
                        port_graph_edges.append((str(output_action.out_port), output_action))

        return port_graph_edges
