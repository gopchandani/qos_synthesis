# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

from config import *
import flow_config as fc
import delay_calculator as dc
import helper_functions as hf
import output_classes as oc
import copy
from collections import defaultdict



class SingleNodeExp:

    def __init__(self, n_flow_each_prio):
        self.flow_specs = []
        self.n_flow_each_prio = n_flow_each_prio

    def create_flow_set(self):
        """ creates flow --> input: number of flows in each priority level """

        # n_rt_flows = n_flow_each_prio * PARAMS.N_PRIO_LEVEL  # total number of RT flows in the systems

        # create flows
        flow_specs = []
        for i in range(PARAMS.N_PRIO_LEVEL):
            for j in range(self.n_flow_each_prio):
                f = fc.get_flow_specs(n_rt_flows=1, n_switch=2, n_host_per_switch=2, nw_diameter=1, prio=i)
                flow_specs.append(f[0])  # since f returns a list

        # update flow ids
        id = 0
        for f in flow_specs:
            f.id = id
            id += 1

        # print flow params
        # for f in flow_specs:
        #     print("ID:", f.id)
        #     print("Source:", f.src)
        #     print("Destination:", f.dst)
        #     print("Period:", f.period)
        #     print("E2E Deadline:", f.e2e_deadline)
        #     print("Prio:", f.prio)

        # save flow_specs
        self.flow_specs = copy.deepcopy(flow_specs)

    def reset_flow_set(self):
        self.flow_specs = []
        self.n_flow_each_prio = -1

    def get_single_node_delay(self, tag_flow_prio, indx=0):
        if tag_flow_prio >= PARAMS.N_PRIO_LEVEL or tag_flow_prio < 0:
            raise ValueError("Invalid priority range!")

        tag_flow_indx = tag_flow_prio*self.n_flow_each_prio + indx

        tag_flow = self.flow_specs[tag_flow_indx]

        qi = dc.get_fifo_delay(tag_flow_indx=tag_flow_indx, flow_specs=self.flow_specs,
                               same_sw_flow_set=self.flow_specs)
        ii = dc.get_priority_interference_delay(tag_flow_indx=tag_flow_indx, flow_specs=self.flow_specs,
                                                same_sw_flow_set=self.flow_specs)

        total_delay = qi + ii

        print("FIFO Delay:", qi)
        print("Priority interference Delay:", ii)
        print("Total delay:", total_delay)
        print("N Flows each queue", self.n_flow_each_prio)
        print("Tag flow period:", tag_flow.period, "Tag flow priority:", tag_flow.prio)
        print("====")

        return total_delay

    def run_single_node_experiment_by_flow_priority(self):

        delay_list = []

        for tag_flow_prio in PARAMS.TAG_FLOW_PRIO_LIST:
            delay = self.get_single_node_delay(tag_flow_prio)
            delay_list.append(delay)

        print("Delay list", delay_list)

        return delay_list


def run_single_node_experiment():
    """ Runs single node experiment with different flow priority and number of flows share same queue """

    all_delay_dict = defaultdict(lambda: defaultdict(dict))

    for n_flow_each_prio in PARAMS.N_FLOW_EACH_PRIO_LIST:
        print("\n#####")
        print("Running for #of flow each queue.. #", n_flow_each_prio)
        print("#####\n")
        for count in range(PARAMS.N_SINGLE_NODE_EXP_SAMPLE_RUN):
            print("====== Sample run.. #", count)
            exp_handler = SingleNodeExp(n_flow_each_prio=n_flow_each_prio)
            exp_handler.create_flow_set()
            delay_list = exp_handler.run_single_node_experiment_by_flow_priority()

            for i in range(len(delay_list)):
                all_delay_dict[n_flow_each_prio][PARAMS.TAG_FLOW_PRIO_LIST[i]][count] = delay_list[i]

    print("Print dict...")
    print(all_delay_dict)

    result = oc.ExportSingleNodeDelay(N_FLOW_EACH_PRIO_LIST=PARAMS.N_FLOW_EACH_PRIO_LIST,
                                      TAG_FLOW_PRIO_LIST=PARAMS.TAG_FLOW_PRIO_LIST,
                                      N_SINGLE_NODE_EXP_SAMPLE_RUN = PARAMS.N_SINGLE_NODE_EXP_SAMPLE_RUN,
                                      all_delay_dict=all_delay_dict)

    # saving results to pickle file
    print("--> Saving result to file...")
    hf.write_object_to_file(result, PARAMS.EXP_SINGLE_NODE_FILENAME)

