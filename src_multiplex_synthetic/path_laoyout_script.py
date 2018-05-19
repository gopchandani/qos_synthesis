# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

import topology_config as tc
import flow_config as fc
import path_generator as pg
import networkx as nx

import random
from config import *


import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
plt.switch_backend('agg')

"""
README: How can I hard code flows:
flow_specs = []

# create bunch of flows with desired params 
f1 = Flow(id=id, src=src, dst=dst, period=period, e2e_deadline=e2e_deadline,
             pckt_size=pckt_size, pkt_processing_time=pkt_processing_time,
             prio=prio)
             
# append to the the flow_specs list
flow_specs.append(f1)


NOTE: make sure 'ID' field is distinct and better to start with zero and increment by 1
"""


def run_path_layout_experiment(topology, flow_specs):

    print("=== Saving topology info (see the toplogy_layout.pdf) ... ===")

    nx.draw_networkx(topology, with_labels=True, font_size=8)

    # plt.show()
    # plt.tight_layout()
    plt.xticks([])
    plt.yticks([])

    plt.savefig("toplogy_layout.pdf")

    print("=== Printing flow specs: ===")
    for f in flow_specs:
        print("\nID:", f.id)
        print("Source:", f.src)
        print("Destination:", f.dst)
        print("Period:", f.period)
        print("E2E Deadline:", f.e2e_deadline)
        print("Packet Size:", f.pckt_size)
        print("Packet Processing time:", f.pkt_processing_time)
        print("Prio:", f.prio)

    path_gen_prop = pg.PathGenerator(topology=topology, flow_specs=flow_specs)

    path_gen_prop.run_path_layout_algo()

    print("\n=== Path info for PROPOSED scheme ===")
    isSched = path_gen_prop.is_schedulable()

    if isSched:
        print("\n=== FLOW SET IS SCHEDULABLE BY PROPOSED SCHEME ====")
    else:
        print("\n===!!! Flow set is NOT SCHEDULABLE by Proposed scheme !!!====")

    # path_gen_sp = pg.PathGenerator(topology=topology, flow_specs=flow_specs)
    #
    # path_gen_sp.run_shortest_path_algo()
    #
    # print("\n=== Path info for SHORTEST PATH scheme ===")
    # isSched = path_gen_sp.is_schedulable()
    #
    # if isSched:
    #     print("\n=== FLOW SET IS SCHEDULABLE BY SHORTEST_PATH SCHEME ====")
    # else:
    #     print("\n===!!! Flow set is NOT SCHEDULABLE by Shortest_Path scheme !!!====")


if __name__ == "__main__":

    # random.seed(3)

    n_switch = PARAMS.NUMBER_OF_SWITCHES
    n_host_per_switch = PARAMS.NUM_HOST_PER_SWITCH
    n_flow_each_prio = 3  # number of flow in each priority level

    # create the topology (you can also hard code it -- a networkx object, similar to RTSS paper)
    topology = tc.TopologyConfiguration(n_switch=n_switch,
                                        n_host_per_switch=n_host_per_switch,
                                        link_bw=PARAMS.LINK_BW,
                                        prop_delay_min=PARAMS.PROP_DELAY_MIN,
                                        prop_delay_max=PARAMS.PROP_DELAY_MAX)
    random_topo = topology.get_random_topology()  # returns a networkx object

    # specify flow specs
    nw_diameter = tc.get_topo_diameter(random_topo)  # get the diameter
    print("Network diameter:", nw_diameter)

    base_e2e_beta = PARAMS.BASE_E2E_BETA_LIST[6]  # set the deadline based on NW topology (base deadline)
    flow_specs = fc.get_flow_specs_by_base_deadline_eq_per_queue(n_prio_level=PARAMS.N_PRIO_LEVEL,
                                                                 n_flow_each_prio=n_flow_each_prio,
                                                                 n_switch=n_switch,
                                                                 n_host_per_switch=n_host_per_switch,
                                                                 nw_diameter=nw_diameter,
                                                                 base_e2e_beta=base_e2e_beta)

    run_path_layout_experiment(random_topo, flow_specs)

    print("Script Finished!!")