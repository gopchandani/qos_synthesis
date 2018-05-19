# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

import topology_config as tc
import flow_config as fc
import delay_calculator as dc
import expermient_handler as eh
import path_generator as pg
import networkx as nx
from config import *
from collections import defaultdict


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
        print("Packet Size:", f.pckt_size)
        print("Packet Processing time:", f.pkt_processing_time)
        print("Prio:", f.prio)


    # print the topology
    print(random_topo.edges(data=True))

    tag_flow_indx = 2
    tag_flow = flow_specs[tag_flow_indx]

    qi = dc.get_fifo_delay(tag_flow_indx=tag_flow_indx, flow_specs=flow_specs, same_sw_flow_set=flow_specs)
    ii = dc.get_priority_interference_delay(tag_flow_indx=tag_flow_indx, flow_specs=flow_specs, same_sw_flow_set=flow_specs)

    # qi = dc.get_fifo_delay(tag_flow_indx=tag_flow_indx, flow_specs=flow_specs, same_sw_flow_set=[])
    # ii = dc.get_priority_interference_delay(tag_flow_indx=tag_flow_indx, flow_specs=flow_specs,
    #                                         same_sw_flow_set=[])


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


def path_layout_experiment():
    topology = tc.TopologyConfiguration(n_switch=PARAMS.NUMBER_OF_SWITCHES,
                                        n_host_per_switch=PARAMS.NUM_HOST_PER_SWITCH,
                                        link_bw=PARAMS.LINK_BW,
                                        prop_delay_min=PARAMS.PROP_DELAY_MIN,
                                        prop_delay_max=PARAMS.PROP_DELAY_MAX)

    random_topo = topology.get_random_topology()  # returns a networkx object


    n_flow_each_prio = 2
    n_switch = topology.n_switch
    n_host_per_switch = topology.n_host_per_switch
    nw_diameter = tc.get_topo_diameter(random_topo)  # get the diameter
    flow_specs = fc.get_flow_specs_equal_per_queue(n_prio_level=PARAMS.N_PRIO_LEVEL,
                                             n_flow_each_prio=n_flow_each_prio,
                                             n_switch=n_switch,
                                             n_host_per_switch=n_host_per_switch,
                                             nw_diameter=nw_diameter)

    print("=== Printing flow specs: ===")
    for f in flow_specs:
        print("\nID:", f.id)
        print("Source:", f.src)
        print("Destination:", f.dst)
        print("E2E Deadline:", f.e2e_deadline)
        print("Packet Size:", f.pckt_size)
        print("Packet Processing time:", f.pkt_processing_time)
        print("Prio:", f.prio)


    # flowid = 2

    path_gen = pg.PathGenerator(topology=random_topo, flow_specs=flow_specs)
    # spath = path_gen.get_shortest_path_by_flow_id(flowid=flowid)
    #
    # print("\n == Shortest path by flowid:", spath, "=== \n")

    # simple_paths =  path_gen.get_all_simple_paths_by_flow_id(flowid=flowid)
    # print("\n == All Simple paths by flowid:\n", simple_paths, "=== \n")

    # feasible_simple_paths = path_gen.get_feasible_simple_paths_by_flow_id(flowid=flowid)
    # print("\n == All Prop-delay Simple paths by flowid:\n", feasible_simple_paths, "=== \n")

    candidate_paths = path_gen.get_all_candidate_paths()

    # print("\n === Candidate paths")
    # print(candidate_paths)
    #
    #
    # print("\n test element")
    # print(candidate_paths[0])
    # print("== \n")
    #
    # # testing remove element
    # pp = candidate_paths[0]
    # rem_element = pp[0]
    #
    # pp.remove(rem_element)
    # candidate_paths[0] = pp
    # print("\n after remove")
    # print(candidate_paths[0])
    # print("== \n")
    #
    # print("\n === Candidate paths (after remove)")
    # print(candidate_paths)


    sw_name = 's1'

    flow_list_sw_name = path_gen.get_flow_list_by_switch_name(candidate_paths=candidate_paths, sw_name=sw_name)

    flowid = 2
    cpd = candidate_paths[flowid][0]  # first cpd
    path = cpd.path

    # delay = path_gen.get_total_delay_by_path(candidate_paths=candidate_paths, flowid=flowid, path=path)
    #
    # print("\n ## Delay is:", delay)

    # test interference index

    # intf_indx = path_gen.get_intf_indx_by_path(candidate_paths=candidate_paths, flowid=flowid, path=path)
    # print("\n ## Intf Index is:", intf_indx)

    # test all interference index
    # for flow in flow_specs:
    #     flowid = flow.id
    #     cpathdata = candidate_paths[flowid]
    #
    #     for cpd in cpathdata:
    #         path = cpd.path
    #         print("\n ## Flowid", flowid, "Path", path)
    #         intf_indx = path_gen.get_intf_indx_by_path(candidate_paths=candidate_paths, flowid=flowid, path=path)
    #         print("II index", intf_indx, "\n")

    path_gen.run_path_layout_algo()
    isSched = path_gen.is_schedulable()

    if isSched:
        print("\n=== FLOW SET IS SCHEDULABLE BY PROPOSED SCHEME ====")


    # test update
    # cpd = candidate_paths[flowid][0]  # first cpd
    # path = cpd.path
    # visited = cpd.visited
    #
    # print("Before:", visited)
    #
    # cpd.visited = True
    # # candidate_paths[flowid][0] = cpd
    # print("After:", candidate_paths[flowid][0].visited)
    #
    # print(candidate_paths[flowid])

    #
    # for cpd in candidate_paths[flowid]:
    #     print("[before] Visited:", cpd.visited, "Path:", cpd.path)
    #
    #
    # # test delete
    # cpd = candidate_paths[flowid][0]  # first cpd
    # candidate_paths[flowid].remove(cpd)
    #
    # for cpd in candidate_paths[flowid]:
    #     print("[After] Visited:", cpd.visited, "Path:", cpd.path)





    # test dictionary

    # candidate_paths = defaultdict(list)
    # for flow in flow_specs:
    #     flowid = flow.id
    #     simplepaths = path_gen.get_feasible_simple_paths_by_flow_id(flowid=flowid)
    #     for p in simplepaths:
    #         cpd = pg.CandidatePathData(path=p)
    #         candidate_paths[flowid].append(cpd)
    #
    #
    # print(candidate_paths)
    #
    # for flowid, candidate_path_data in candidate_paths.items():
    #     for cpd in candidate_path_data:
    #         path = cpd.path
    #         intf_idx = cpd.intf_indx
    #         print("flowid:", flowid, "II", intf_idx, "path:", path)


    # print the topology
    print("\n\n printing topo info...")
    print(random_topo.edges(data=True))

    print("=== Printing flow specs: ===")
    for f in flow_specs:
        print("\nID:", f.id)
        print("Source:", f.src)
        print("Destination:", f.dst)
        print("E2E Deadline:", f.e2e_deadline)
        print("Packet Size:", f.pckt_size)
        print("Packet Processing time:", f.pkt_processing_time)
        print("Prio:", f.prio)
        print("Path:", f.path)





if __name__ == "__main__":

    #topology_test()
    # flow_test()
    # delay_test()
    # single_node_exp_test()
    path_layout_experiment()


    print("script finished!!")
