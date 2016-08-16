__author__ = 'Rakesh Kumar'

import sys
sys.path.append("./")

from experiment import Experiment
from network_configuration import NetworkConfiguration


class QosDemo(Experiment):

    def __init__(self,
                 num_iterations,
                 network_configurations):

        super(QosDemo, self).__init__("number_of_hosts", num_iterations)
        self.network_configurations = network_configurations

    def trigger(self):

        for nc in self.network_configurations:
            print "network_configuration:", nc


def prepare_network_configurations(num_hosts_per_switch_list):
    nc_list = []
    for hps in num_hosts_per_switch_list:

        # nc = NetworkConfiguration("ryu",
        #                           "clostopo",
        #                           {"fanout": 2,
        #                            "core": 1,
        #                            "num_hosts_per_switch": hps},
        #                           conf_root="configurations/",
        #                           synthesis_name="AboresceneSynthesis",
        #                           synthesis_params={"apply_group_intents_immediately": True})

        # nc = NetworkConfiguration("ryu",
        #                          "ring",
        #                          {"num_switches": 12,
        #                           "num_hosts_per_switch": hps},
        #                          conf_root="configurations/",
        #                          synthesis_name="AboresceneSynthesis",
        #                          synthesis_params={"apply_group_intents_immediately": True})

        nc = NetworkConfiguration("ryu",
                                 "linear",
                                 {"num_switches": 2,
                                  "num_hosts_per_switch": hps},
                                 conf_root="configurations/",
                                 synthesis_name="SynthesizeQoS",
                                 synthesis_params={"apply_group_intents_immediately": True})

        nc.setup_network_graph(mininet_setup_gap=1, synthesis_setup_gap=1)

        nc_list.append(nc)

    return nc_list


def main():

    num_iterations = 1
    num_hosts_per_switch_list = [2]#[2, 4, 6, 8, 10]
    network_configurations = prepare_network_configurations(num_hosts_per_switch_list)
    exp = QosDemo(num_iterations, network_configurations)

    exp.trigger()

if __name__ == "__main__":
    main()