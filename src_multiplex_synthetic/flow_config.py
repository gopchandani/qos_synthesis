# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

import itertools
import random
import helper_functions as hf
import math
import copy
from config import *


class Flow:

    def __init__(self, id, src, dst, period, e2e_deadline, pckt_size, pkt_processing_time, prio, flowclass="RT"):
        self.id = id
        self.src = src
        self.dst = dst
        self.period = period
        self.e2e_deadline = e2e_deadline
        self.pckt_size = pckt_size
        self.pkt_processing_time = pkt_processing_time
        self.prio = prio
        self.flowclass = flowclass
        self.bw_req = pckt_size/period
        self.path = []  # will be updated later


def get_flow_by_param(id, indx, nxtindx, period, e2e_deadline, prio):
    """ Returns an individual flow class (will be appended in the set of flows later) """

    src = "h" + str(indx[0]) + str(indx[1])
    dst = "h" + str(nxtindx[0]) + str(nxtindx[1])

    pktindx = random.randint(0, len(PARAMS.PKT_SIZE_LIST)-1)

    pckt_size = PARAMS.PKT_SIZE_LIST[pktindx]
    pkt_processing_time = PARAMS.PKT_PROCESSING_TIME_LIST[pktindx]

    f = Flow(id=id, src=src, dst=dst, period=period, e2e_deadline=e2e_deadline,
             pckt_size=pckt_size, pkt_processing_time=pkt_processing_time,
             prio=prio)

    return f


def get_flow_specs_by_base_delay(n_rt_flows, n_switch, n_host_per_switch, hp_flow_e2e_deadline):
    """
    Returns the set of flows
    """

    flow_specs = []  # a set of flows with parameters

    flowlist = list(itertools.product(range(1, n_switch + 1), range(1, n_host_per_switch + 1)))

    # generate random indices (#of_RT_flows)
    index_list = [random.randint(0, len(flowlist) - 1) for i in range(n_rt_flows)]

    period_list = [random.uniform(PARAMS.PERIOD_MIN, PARAMS.PERIOD_MAX) for i in range(n_rt_flows)]
    period_list.sort()  # sorted (HP flows gets shorter period)

    print("Period list is", period_list)

    e2e_deadline = hp_flow_e2e_deadline  # init delay variable (will be changed for each flow)

    for i in range(n_rt_flows):
        indx = flowlist[index_list[i]]
        rnd = list(range(1, indx[0])) + list(range(indx[0]+1, n_switch+1))
        nxtindx = (random.choice(rnd), random.randint(1, n_host_per_switch))

        f = get_flow_by_param(indx=indx, nxtindx=nxtindx, period=period_list[i],e2e_deadline=e2e_deadline, prio=i)

        e2e_deadline += PARAMS.DELAY_DELTA  # update deadline for next flow

        flow_specs.append(f)

    return flow_specs


def get_flow_specs(n_rt_flows, n_switch, n_host_per_switch, nw_diameter, prio=None):
    """
    Returns the set of flows
    """

    flow_specs = []  # a set of flows with parameters

    flowlist = list(itertools.product(range(1, n_switch + 1), range(1, n_host_per_switch + 1)))

    # generate random indices (#of_RT_flows)
    index_list = [random.randint(0, len(flowlist) - 1) for i in range(n_rt_flows)]

    # util_list = hf.UUniFast(n_rt_flows, PARAMS.BASE_UTIL)
    # print(util_list)
    # period_list = [math.ceil(PARAMS.PCKT_PROCESSING_TIME/util) for util in util_list]

    period_list = [random.randint(PARAMS.PERIOD_MIN, PARAMS.PERIOD_MAX) for i in range(n_rt_flows)]
    period_list.sort()  # sorted (HP flows gets shorter period)

    # deadline_list = [nw_diameter * (PARAMS.PROP_DELAY_MAX + period_list[i]) for i in range(n_rt_flows)]
    deadline_list = copy.deepcopy(period_list)  # deadline = period

    # print("Period list is", period_list)
    # print("Deadline list is", deadline_list)

    # decide whether we use a given priority or generate priority randomly
    GEN_PRIO = False
    if prio is None:
        GEN_PRIO = True

    for i in range(n_rt_flows):
        indx = flowlist[index_list[i]]
        rnd = list(range(1, indx[0])) + list(range(indx[0]+1, n_switch+1))
        nxtindx = (random.choice(rnd), random.randint(1, n_host_per_switch))

        if GEN_PRIO:
            prio = random.randint(0, PARAMS.N_PRIO_LEVEL - 1)  # set a priority randomly

        f = get_flow_by_param(id=i, indx=indx, nxtindx=nxtindx, period=period_list[i],e2e_deadline=deadline_list[i], prio=prio)

        flow_specs.append(f)

    return flow_specs


def get_flow_specs_equal_per_queue(n_prio_level, n_flow_each_prio, n_switch, n_host_per_switch, nw_diameter):
    """Create flows (each queue contains fixed number of flows """

    # create flows
    flow_specs = []
    for i in range(n_prio_level):
        for j in range(n_flow_each_prio):
            f = get_flow_specs(n_rt_flows=1, n_switch=n_switch, n_host_per_switch=n_host_per_switch,
                               nw_diameter=nw_diameter, prio=i)
            flow_specs.append(f[0])  # since f returns a list

    # update flow ids
    id = 0
    for f in flow_specs:
        f.id = id
        id += 1

    return flow_specs
