# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

import networkx as nx
import copy
from collections import defaultdict
import delay_calculator as dc
from config import *


class CandidatePathData():
    """ Save candidate paths data """
    def __init__(self, flowid, path, intf_indx=0, visited=False):
        self.flowid = flowid
        self.path = path
        self.intf_indx = intf_indx
        self.visited = visited


def get_candidate_path_dict_size(candidate_paths):
    count = 0
    for flowid, candidate_path_data in candidate_paths.items():
        for cpd in candidate_path_data:
            count += 1

    return count


class PathGenerator:
    """ Helper class for path generator"""

    def __init__(self, topology, flow_specs, _debug=True):
        self.topology = copy.deepcopy(topology)  # create own copy
        self.flow_specs = copy.deepcopy(flow_specs)
        self.DEBUG = _debug  # if true print output

    def get_shortest_path_by_flow_id(self, flowid):

        # some error checking
        flow = self.get_flow_by_id(flowid)
        if flow is None:
            print("Invalid flow ID!!")
            return None

        src = flow.src
        dst = flow.dst
        path = nx.shortest_path(self.topology, source=src, target=dst)

        return path

    def get_flow_by_id(self, flowid):

        flow = None
        for f in self.flow_specs:
            if f.id == flowid:
                flow = copy.deepcopy(f)
                break

        return flow

    def get_flow_idex_by_id(self, flowid):

        indx = None
        for i in range(len(self.flow_specs)):
            if flowid == i:
                indx = i
                break

        return indx

    def get_all_simple_paths_by_flow_id(self, flowid):

        # some error checking
        flow = self.get_flow_by_id(flowid)
        if flow is None:
            print("Invalid flow ID!!")
            return None

        src = flow.src
        dst = flow.dst
        paths = nx.all_simple_paths(self.topology, source=src, target=dst)
        paths = list(paths)  # convert generator to a list

        return paths

    def get_all_simple_paths_by_src_dst(self, src, dst):

        paths = nx.all_simple_paths(self.topology, source=src, target=dst)
        paths = list(paths)  # convert generator to a list

        return paths

    def get_feasible_simple_paths_by_flow_id(self, flowid):

        # some error checking
        flow = self.get_flow_by_id(flowid)
        if flow is None:
            print("Invalid flow ID!!")
            return None

        src = flow.src
        dst = flow.dst

        paths = self.get_all_simple_paths_by_src_dst(src, dst)

        if paths is None:
            return None

        feasible_paths = []
        for path in paths:
            pdelay_sum = 0
            for i in range(len(path)-1):
                e0 = path[i]
                e1 = path[i+1]

                pdelay = self.topology[e0][e1]['prop_delay']
                pdelay_sum += pdelay

            if pdelay_sum <= flow.e2e_deadline:
                p = copy.deepcopy(path)  # for safety copy to a new object
                feasible_paths.append(p)

        return feasible_paths

    def get_all_candidate_paths(self):

        """Returns all possible candidate paths (for all flows)
        A dictionary. Key: flowid, Value: the class instance CandidatePathData """

        candidate_paths = defaultdict(list)
        for flow in self.flow_specs:
            flowid = flow.id
            simplepaths = self.get_feasible_simple_paths_by_flow_id(flowid)
            # print("flowid:", flowid, "#of simple paths", len(simplepaths))

            # in case no simple path found
            if len(simplepaths) == 0:
                simplepaths = nx.all_shortest_paths(self.topology, source=flow.src, target=flow.dst)
                simplepaths = list(simplepaths)
                # print("Get shortest paths. Flowid:", flowid, "length:", len(simplepaths))
                # print("simplepaths", simplepaths)

            for p in simplepaths:
                cpd = CandidatePathData(flowid=flowid, path=p)
                candidate_paths[flowid].append(cpd)

        # print("Printing Candidate paths:")
        # self.print_candidate_paths(candidate_paths)
        return candidate_paths

    def get_flow_list_by_switch_name(self, candidate_paths, sw_name):
        """ Returns the set of flows using the same switch for a given set of candidate paths"""

        flowid_list = []
        flow_list = []

        # get flowids that routed through the switch
        for flowid, candidate_path_data in candidate_paths.items():
            for cpd in candidate_path_data:
                path = cpd.path
                for node in path:
                    if node == sw_name:
                        flowid_list.append(flowid)

        # remove duplicates
        flowid_list = list(set(flowid_list))

        # create flow list from flow ids

        for fid in flowid_list:
            flow = self.get_flow_by_id(flowid=fid)
            flow_list.append(flow)

        return flow_list

    def get_total_delay_by_path(self, candidate_paths, flowid, path):

        # print("Flowid:", flowid, "Given Path: ", path)
        path_delay = 0

        tag_flow_indx = self.get_flow_idex_by_id(flowid=flowid)  # no error checking (assuming flowid is correct)

        for node in path:
            # this is a switch
            if 's' in node:
                same_sw_flow_set = self.get_flow_list_by_switch_name(candidate_paths=candidate_paths,
                                                                     sw_name=node)

                # FIFO delay
                # qi = dc.get_fifo_delay_by_pck_size(tag_flow_indx=tag_flow_indx, flow_specs=self.flow_specs,
                #                                     same_sw_flow_set=same_sw_flow_set)
                qi = dc.get_fifo_delay(tag_flow_indx=tag_flow_indx, flow_specs=self.flow_specs,
                                       same_sw_flow_set=same_sw_flow_set)

                # Priority interference delay
                ii = dc.get_priority_interference_delay(tag_flow_indx=tag_flow_indx, flow_specs=self.flow_specs,
                                                        same_sw_flow_set=same_sw_flow_set)

                # print("FIFO delay:", qi)
                # print("Intf delay:", ii)

                delay = qi + ii
                path_delay += delay

        # now add propagation delay
        prop_delay = self.get_prop_delay_by_path(path)

        path_delay = path_delay + prop_delay

        return path_delay

    def get_prop_delay_by_path(self, path):

        prop_delay = 0
        for i in range(len(path) - 1):
            e0 = path[i]
            e1 = path[i + 1]

            # if this is a switch-switch link
            if 's' in e0 and 's' in e1:
                pdelay = self.topology[e0][e1]['prop_delay']
                prop_delay += pdelay

        return prop_delay

    def get_flow_list_by_edge(self, candidate_paths, node0, node1):
        """ Returns the set of flows using the same switch for a given set of candidate paths"""

        flowid_list = []
        flow_list = []

        # get flowids that routed through the link (node0, node1)
        for flowid, candidate_path_data in candidate_paths.items():
            for cpd in candidate_path_data:
                path = cpd.path
                for i in range(len(path) - 1):
                    e0 = path[i]
                    e1 = path[i + 1]

                    if e0 == node0 and e1 == node1:
                        flowid_list.append(flowid)
                        break

        # remove duplicates
        flowid_list = list(set(flowid_list))

        # create flow list from flow ids

        for fid in flowid_list:
            flow = self.get_flow_by_id(flowid=fid)
            flow_list.append(flow)

        return flow_list

    def get_residual_bw_by_edge(self, candidate_paths, node0, node1):
        link_bw = self.topology[node0][node1]['link_bw']
        flow_list = self.get_flow_list_by_edge(candidate_paths, node0, node1)
        sum_bw_req = 0
        for f in flow_list:
            sum_bw_req += f.bw_req

        res_bw = link_bw - sum_bw_req

        return res_bw

    def get_bw_utilization_by_path(self, candidate_paths, flowid, path):

        tag_flow = self.get_flow_by_id(flowid=flowid)

        bw_util = 0

        for i in range(len(path) - 1):
            e0 = path[i]
            e1 = path[i + 1]

            # if this is a switch-switch link
            if 's' in e0 and 's' in e1:
                res_bw = self.get_residual_bw_by_edge(candidate_paths, e0, e1)

                if res_bw == 0:  # if no residual BW, set to large number
                    bw_util = PARAMS.LARGE_NUMBER
                else:
                    util = tag_flow.pckt_size/res_bw
                    bw_util += util  # sum-up for the path

        # if negative, set to a large value
        if bw_util < 0:
            bw_util = PARAMS.LARGE_NUMBER

        return bw_util

    def get_intf_indx_by_path(self, candidate_paths, flowid, path):

        # print("Flowid:", flowid, "Given Path: ", path)

        tag_flow = self.get_flow_by_id(flowid=flowid)  # no error checking (assuming flowid is correct)

        total_delay = self.get_total_delay_by_path(candidate_paths, flowid, path)
        prop_delay = self.get_prop_delay_by_path(path)
        queuing_delay = total_delay - prop_delay

        bw_util = self.get_bw_utilization_by_path(candidate_paths, flowid, path)

        intf_indx = tag_flow.e2e_deadline - prop_delay + queuing_delay + bw_util

        return intf_indx

    def terminate_loop(self, candidate_paths):
        """ The function returns whether we can terminate the loop in path generation """

        for flowid, candidate_path_data in candidate_paths.items():
            for cpd in candidate_path_data:
                if not cpd.visited:
                    return False

        # for flowid, candidate_path_data in candidate_paths.items():
        #     if len(candidate_path_data) > 1:
        #         return False
        return True

    def print_candidate_paths(self, candidate_paths):

        cnt = 0
        for flow in self.flow_specs:
            flowid = flow.id
            cpathdata = candidate_paths[flowid]

            for cpd in cpathdata:
                path = cpd.path
                print("Entry", cnt, "## Flowid", flowid,  "Path", path, "II:", cpd.intf_indx, "visited:", cpd.visited)
                cnt +=1

    def update_candiate_paths(self, candidate_paths):
        """ Update candidate path dictionary:
            Deletes the path with max II,
            set 'path' (in 'Flow' variable) if the path is the only available path for the flow
            Update 'visited' flag"""

        max_ii = -1 * PARAMS.LARGE_NUMBER
        max_fid = -1
        max_cpd = None
        for flowid, candidate_path_data in candidate_paths.items():
            for cpd in candidate_path_data:
                if not cpd.visited:
                    path = cpd.path
                    intf_indx = self.get_intf_indx_by_path(candidate_paths=candidate_paths, flowid=flowid, path=path)
                    cpd.intf_indx = intf_indx  # update intf_indx
                    # print("Flow id:", flowid, "II Index:", intf_indx, "visited", cpd.visited)
                    if intf_indx > max_ii:
                        max_ii = intf_indx
                        max_fid = flowid
                        max_cpd = cpd

        # print("\n Before: ===")
        # self.print_candidate_paths(candidate_paths)

        if max_fid >= 0:
            if self.DEBUG:
                print("MaxII flowid:", max_fid, "Max II:", max_ii, "MaxII path:", max_cpd.path)

            cpdlist = candidate_paths[max_fid]

            # the flow has more than one candidate path
            if len(cpdlist) > 1:
                # remove the path from list
                candidate_paths[max_fid].remove(max_cpd)

            elif len(cpdlist) == 1:
                # this is the only path for the flow
                # candidate_paths[max_fid].remove(max_cpd)
                max_cpd.visited = True
                flowindx = self.get_flow_idex_by_id(max_fid)
                self.flow_specs[flowindx].path = copy.deepcopy(max_cpd.path)

                if self.DEBUG:
                    print("Got last candidate path for Flow#", max_fid, ":: set the path variable and update residual BW.")

                # update residual bandwidth
                for i in range(len(max_cpd.path) - 1):
                    e0 = max_cpd.path[i]
                    e1 = max_cpd.path[i + 1]

                    # if this is a switch-switch link
                    if 's' in e0 and 's' in e1:
                        self.topology[e0][e1]['link_bw'] -= self.flow_specs[flowindx].bw_req

            # print("\n After: ===")
            # self.print_candidate_paths(candidate_paths)

    def run_path_layout_algo(self):
        """ This is the main algorithm that generates path"""

        candidate_paths = self.get_all_candidate_paths()

        isRunnable = self.check_all_flow_has_candidate_path(candidate_paths)
        if not isRunnable:
            raise Exception("Not all flow gets candidate path -- algorithm will not work. Mark flowset UNSCHEDULABLE.")
        else:
            print("\nCandidate path generation complete. All flow has at least one candidate path.")

        all_cand_dict_size = get_candidate_path_dict_size(candidate_paths)
        print("# of Candidate paths:", all_cand_dict_size)

        if self.DEBUG:
            print("Running path layout algorithm (pruning path with max interference) ...")

        count = 0
        while True:
            if self.DEBUG:
                print("\n==== Iteration #", count, "====")

            count += 1
            self.update_candiate_paths(candidate_paths)

            # print("Printing candidate paths...")
            # self.print_candidate_paths(candidate_paths)

            if self.terminate_loop(candidate_paths):
                print("Done with path layout!! Terminating loop...")
                # print("Printing candidate paths...")
                # self.print_candidate_paths(candidate_paths)
                break

            if count > all_cand_dict_size+1:
                print("!!! Loop running more than #of candidate paths. Terminating... [Flow set is not schedulable] !!!")

    def check_all_flow_has_candidate_path(self, candidate_paths):

        cpath_fid = list(candidate_paths.keys())
        fid_list = []
        for f in self.flow_specs:
            fid_list.append(copy.deepcopy(f.id))

        if set(cpath_fid) == set(fid_list):
            return True

        return False


    def is_schedulable(self):
        """Check the schedulability of the flow-set"""
        for f in self.flow_specs:
            if not f.path:
                print("== Not all flow get path assigned! Flow set is unschedulable! ==")
                return False

        isSched = True
        # print paths
        if self.DEBUG:
            for f in self.flow_specs:
                print("Flowid:", f.id, "Path:", f.path)

        # prepare a dict to store all assigned paths
        allocated_paths = defaultdict(list)
        for f in self.flow_specs:
            flowid = f.id
            path = f.path
            cpd = CandidatePathData(flowid=flowid, path=path)
            allocated_paths[flowid].append(cpd)

        # check delay and BW constraints:
        for f in self.flow_specs:
            total_delay = self.get_total_delay_by_path(allocated_paths, f.id, f.path)
            if self.DEBUG:
                print("\nFlowid:", f.id, "Prio:", f.prio, "Observed Delay:", total_delay, "E2E deadline:", f.e2e_deadline)
            if total_delay > f.e2e_deadline:
                # print("####  Delay Constraint violated for Flowid:", f.id,
                #       " ==> Deadline:", f.e2e_deadline, "Observed Delay:", total_delay, "####")
                if self.DEBUG:
                    print("==> Delay Constraint violated for Flowid:", f.id)
                # return False
                isSched = False

            for i in range(len(f.path) - 1):
                e0 = f.path[i]
                e1 = f.path[i + 1]

                # if this is a switch-switch link
                if 's' in e0 and 's' in e1:
                    if self.topology[e0][e1]['link_bw'] < 0:
                        # print("####  BW Constraint violated for Flow:", f.id,
                        #       "Link BW:", self.topology[e0][e1]['link_bw'], "####")
                        if self.DEBUG:
                            print("==> BW Constraint violated for Flow:", f.id, "Link:", e0, "-", e1)
                        # return False
                        isSched = False

        # return True
        return isSched

    def run_shortest_path_algo(self):

        nx.set_edge_attributes(self.topology, 'cost', 1)  # add a new attribute COST

        # print("\n\n printing topo info...")
        # print(self.topology.edges(data=True))

        for flow in self.flow_specs:
            try:
                spath = nx.shortest_path(self.topology, source=flow.src, target=flow.dst, weight="cost")
                flow.path = copy.deepcopy(spath)  # update path
            except nx.NetworkXNoPath:
                print("No SP returned by NetworkX!")
                flow.path = []
                continue

            # update residual bandwidth
            for i in range(len(spath) - 1):
                e0 = spath[i]
                e1 = spath[i + 1]

                # if this is a switch-switch link
                if 's' in e0 and 's' in e1:
                    self.topology[e0][e1]['link_bw'] -= flow.bw_req
                    if self.topology[e0][e1]['link_bw'] <= 0:
                        print("\nSP: Link overloaded! -> Current flow", flow.id)
                        self.topology[e0][e1]['link_bw'] = PARAMS.LARGE_NUMBER  # set the high cost for that link
