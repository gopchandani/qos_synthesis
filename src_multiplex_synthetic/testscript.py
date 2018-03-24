# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

import topology_config as tc
import flow_config as fc
import delay_calculator as dc
import expermient_handler as eh
import networkx as nx
from config import *


def topology_test():
    topology = tc.TopologyConfiguration(n_switch=PARAMS.NUMBER_OF_SWITCHES,
                                        n_host_per_switch=PARAMS.NUM_HOST_PER_SWITCH,
                                        link_bw=PARAMS.LINK_BW,
                                        prop_delay_min=PARAMS.PROP_DELAY_MIN,
                                        prop_delay_max=PARAMS.PROP_DELAY_MAX)

    random_topo = topology.get_random_topology()  # returns a networkx object

    # for i in random_topo.edges():
    #     print("Connecton name1:", i[0])
    #     print("Connecton name2:", i[1])
    #     bw = random_topo[i[0]][i[1]]['link_bw']
    #     prop_delay = random_topo[i[0]][i[1]]['prop_delay']
    #     print("bw:", bw, "prob_delay:", prop_delay)
    #
    #     random_topo[i[0]][i[1]]['link_bw'] += 5

    # testing to see whether update is affected
    # print(random_topo.edges(data=True))

    # print the topology
    print(random_topo.edges(data=True))

    # print adjacency list to screen
    print('adjacency matrix')
    A = nx.adjacency_matrix(random_topo)
    print(A.todense())


def flow_test():
    topology = tc.TopologyConfiguration(n_switch=PARAMS.NUMBER_OF_SWITCHES,
                                        n_host_per_switch=PARAMS.NUM_HOST_PER_SWITCH,
                                        link_bw=PARAMS.LINK_BW,
                                        prop_delay_min=PARAMS.PROP_DELAY_MIN,
                                        prop_delay_max=PARAMS.PROP_DELAY_MAX)

    random_topo = topology.get_random_topology()  # returns a networkx object
    nw_diameter = tc.get_topo_diameter(random_topo)  # get the diameter

    print("Diameter:", nw_diameter)

    base_delay_budget = 0.003
    hp_flow_e2e_deadline = tc.get_hp_flow_delay_budget(random_topo, base_delay_budget)
    n_rt_flows = 15
    n_switch = topology.n_switch
    n_host_per_switch = topology.n_host_per_switch

    # flow_specs = fc.get_flow_specs(n_rt_flows, n_switch, n_host_per_switch, hp_flow_e2e_deadline)
    flow_specs = fc.get_flow_specs(n_rt_flows, n_switch, n_host_per_switch, nw_diameter, prio=None)

    for f in flow_specs:
        print("Source:", f.src)
        print("Destination:", f.dst)
        print("E2E Deadline:", f.e2e_deadline)
        print("Prio:", f.prio)


    # print the topology
    print(random_topo.edges(data=True))


def delay_test():
    topology = tc.TopologyConfiguration(n_switch=PARAMS.NUMBER_OF_SWITCHES,
                                        n_host_per_switch=PARAMS.NUM_HOST_PER_SWITCH,
                                        link_bw=PARAMS.LINK_BW,
                                        prop_delay_min=PARAMS.PROP_DELAY_MIN,
                                        prop_delay_max=PARAMS.PROP_DELAY_MAX)

    random_topo = topology.get_random_topology()  # returns a networkx object
    nw_diameter = tc.get_topo_diameter(random_topo)  # get the diameter

    print("Diameter:", nw_diameter)

    n_rt_flows = 25

    n_switch = topology.n_switch
    n_host_per_switch = topology.n_host_per_switch

    flow_specs = fc.get_flow_specs(n_rt_flows, n_switch, n_host_per_switch, nw_diameter, prio=None)
    # flow_specs = fc.get_flow_specs(n_rt_flows, n_switch, n_host_per_switch, nw_diameter, prio=2)

    for f in flow_specs:
        print("ID:", f.id)
        print("Source:", f.src)
        print("Destination:", f.dst)
        print("E2E Deadline:", f.e2e_deadline)
        print("Prio:", f.prio)


    # print the topology
    print(random_topo.edges(data=True))

    tag_flow_indx = 2
    tag_flow = flow_specs[tag_flow_indx]

    qi = dc.get_fifo_delay(tag_flow_indx=tag_flow_indx, flow_specs=flow_specs, same_sw_flow_set=flow_specs)
    ii = dc.get_priority_interference_delay(tag_flow_indx=tag_flow_indx, flow_specs=flow_specs, same_sw_flow_set=flow_specs)

    print("FIFO Delay:", qi)
    print("Priority interference Delay:", ii)
    print("Total Delay:", qi+ii)
    print("Tag flow period:", tag_flow.period, "Tag flow priority:", tag_flow.prio)

    ntag_flow = 0
    for fk in flow_specs:
        if tag_flow.prio == fk.prio:
            ntag_flow += 1

    print("Total Number of flow with tag flow prio:", ntag_flow)


def single_node_exp_test():

    n_flow_each_prio = 2
    # tag_flow_prio = 7
    # exp_handler = eh.SingleNodeExp(n_flow_each_prio=n_flow_each_prio)
    # exp_handler.create_flow_set()
    # exp_handler.run_single_node_experiment_by_flow_priority()

    eh.run_single_node_experiment()



if __name__ == "__main__":

    #topology_test()
    # flow_test()
    # delay_test()
    single_node_exp_test()


    print("script finished!!")
