# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

import networkx as nx
import random
from config import *


class TopologyConfiguration(object):

    def __init__(self, n_switch, n_host_per_switch, link_bw, prop_delay_min, prop_delay_max):
        self.n_switch = n_switch
        self.n_host_per_switch = n_host_per_switch
        self.link_bw = link_bw
        self.prop_delay_min = prop_delay_min
        self.prop_delay_max = prop_delay_max

    def get_random_link_data(self):
        propdelay = random.randint(self.prop_delay_min, self.prop_delay_max)  # get a random delay
        link_data = {'prop_delay': propdelay, 'link_bw': self.link_bw}

        return link_data

    def get_random_topology(self):

        """
        Creates a random topology similar to our RTSS17 paper.
        Returns a networkx graph object
        """
        nw_graph = nx.Graph()
        switch_names = []

        # setup the switchs
        for i in range(self.n_switch):
            nw_graph.add_node("s" + str(i + 1))
            switch_names.append("s" + str(i + 1))
            # add hosts per switch
            for j in range(self.n_host_per_switch):
                nw_graph.add_node("h" + str(i + 1) + str(j + 1))

                # add link
                link_data = self.get_random_link_data()
                nw_graph.add_edge("s" + str(i + 1),
                                  "h" + str(i + 1) + str(j + 1),
                                  prop_delay=link_data['prop_delay'],
                                  link_bw=link_data['link_bw'])

        # Add links between switches
        if self.n_switch > 1:
            for i in range(self.n_switch - 1):
                link_data = self.get_random_link_data()
                nw_graph.add_edge(switch_names[i], switch_names[i + 1],
                                  prop_delay=link_data['prop_delay'],
                                  link_bw=link_data['link_bw'])

            # Form a ring only when there are more than two switches
            if self.n_switch > 2:
                link_data = self.get_random_link_data()
                nw_graph.add_edge(switch_names[0], switch_names[-1],
                                  prop_delay=link_data['prop_delay'],
                                  link_bw=link_data['link_bw'])

                # create some random links
                nodelist = noncontiguoussample(self.n_switch - 1,
                                                    int(self.n_switch / 2.0))

                for i in range(len(nodelist) - 1):
                    switch_names[nodelist[i]]

                    link_data = self.get_random_link_data()

                    nw_graph.add_edge(switch_names[nodelist[i]], switch_names[nodelist[i + 1]],
                                      prop_delay=link_data['prop_delay'],
                                      link_bw=link_data['link_bw'])

        return nw_graph


def noncontiguoussample(n, k):
    # How many numbers we're not picking
    total_skips = n - k

    # Distribute the additional skips across the range
    skip_cutoffs = random.sample(range(total_skips + 1), k)
    skip_cutoffs.sort()

    # Construct the final set of numbers based on our skip distribution
    samples = []
    for index, skip_spot in enumerate(skip_cutoffs):
        # This is just some math-fu that translates indices within the
        # skips to values in the overall result.
        samples.append(1 + index + skip_spot)

    return samples


def get_hp_flow_delay_budget(topology, base_delay_budget):

    """
    This is same as RTSS17 Paper
    """
    diameter = nx.diameter(topology)

    hp_e2e_deadline = base_delay_budget * diameter  # vary with topology as Rakesh K. mentioned

    hp_e2e_deadline = hp_e2e_deadline + PARAMS.BASE_DELAY_BUDGET_PAD*hp_e2e_deadline

    return hp_e2e_deadline


def get_base_flow_delay_budget(topology):

    """
    Base delay depends on link propagation delay
    """

    diameter = nx.diameter(topology)

    base_e2e_deadline = PARAMS.PROP_DELAY_MAX * diameter  # vary with topology as Rakesh K. mentioned

    base_e2e_deadline = base_e2e_deadline + PARAMS.BASE_DELAY_BUDGET_PAD*base_e2e_deadline

    return base_e2e_deadline


def get_topo_diameter(topology):
    """ returns the diameter of the topology """

    diameter = nx.diameter(topology)
    return diameter
