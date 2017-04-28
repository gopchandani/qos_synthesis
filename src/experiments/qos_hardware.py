__author__ = 'Rakesh Kumar'

import os
import matplotlib.pyplot as plt
import sys
import time
from collections import defaultdict
from itertools import permutations
import subprocess

sys.path.append("./")

from controller_man import ControllerMan
from experiment import Experiment
from network_configuration_hardware import NetworkConfiguration
from flow_specification import FlowSpecification
from model.match import Match

sys.path.append("./")
sys.path.append("../")

class QosDemo(Experiment):

    def __init__(self,
                 network_configurations,
                 num_iterations,
                 num_measurements):

        super(QosDemo, self).__init__("number_of_hosts", 2)
        self.network_configurations = network_configurations
        self.controller_port = 6633
        self.num_iterations = num_iterations
        self.num_measurements = num_measurements


    def trigger(self):
        for nc in self.network_configurations:
            nc.synthesis.clear_all_flows()
            nc.setup_network_graph(mininet_setup_gap=1, synthesis_setup_gap=1)
            nc.init_flow_specs()
            nc.synthesis.synthesize_flow_specifications(nc.flow_specs)
            self.measure_flow_rates(nc)

    def measure_flow_rates(self, nc):

        servers = [
            {"ip": "192.168.0.1",
             "usr": "sdn",
             "psswd": "sdn123"},
            {"ip": "192.168.0.2",
             "usr": "sdn",
             "psswd": "sdn123"},
        ]

        clients = [
            {"ip": "192.168.0.3",
             "usr": "sdn",
             "psswd": "sdn123"},
            {"ip": "192.168.0.4",
             "usr": "sdn",
             "psswd": "sdn123"},
        ]

        for i in range(self.num_iterations):
            print "iteration:", i + 1

            for j in range(self.num_measurements):

                max_fs_duration = 0

                for fs in nc.flow_specs:

                    if not fs.measurement_rates:
                        continue

                    netperf_cmd = fs.consturct_netperf_cmd_str(fs.measurement_rates[j])
                    # launch servers
                    for serv in servers:
                        subprocess.call("sshpass -p '%s' ssh %s@%s '/usr/local/bin/netserver &'"
                               % serv["psswd"], serv["usr"], serv["ip"])

                    for client in clients:

                        subprocess.call("sshpass -p '%s' ssh %s@%s '%s > out_%s.txt &'"
                               % client["psswd"], client["usr"], client["ip"],
                               netperf_cmd, str(j))
                    # server_output = fs.mn_dst_host.cmd("/usr/local/bin/netserver")
                    # client_output = fs.mn_src_host.cmd(fs.construct_netperf_cmd_str(fs.measurement_rates[j]))

                    if fs.tests_duration > max_fs_duration:
                        max_fs_duration = fs.tests_duration

                # Sleep for 5 seconds more than flow duration to make sure netperf has finished.
                time.sleep(max_fs_duration + 5)

                for fs in nc.flow_specs:

                    if not fs.measurement_rates:
                        continue

                    for client in clients:
                        output = subprocess.check_output("sshpass -p '%s' ssh %s@s 'cat out_%s.txt'"
                                                         % client["psswd"],
                                                         client["usr"],
                                                         client["ip"],
                                                         str(j))
                        fs.measurements[fs.measurement_rates[j]].append(fs.parse_measurements(output))



    def plot_qos(self):

        f, (ax2, ax3) = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(6.0, 3.0))
        f.tight_layout()

        data_xticks = self.network_configurations[0].flow_specs[0].measurement_rates
        data_xtick_labels = [str(x) for x in data_xticks]

        # self.plot_lines_with_error_bars(ax1,
        #                                 "Throughput",
        #                                 "",
        #                                 "Throughput(Mbps)",
        #                                 "(a)",
        #                                 y_scale='linear',
        #                                 x_min_factor=0.98,
        #                                 x_max_factor=1.02,
        #                                 y_min_factor=0.01,
        #                                 y_max_factor=1,
        #                                 xticks=data_xticks,
        #                                 xtick_labels=data_xtick_labels)
        #
        # ax1.set_ylim(40, 47.5)

        self.plot_lines_with_error_bars(ax2,
                                        "Mean Latency",
                                        "Flow Rate (Mbps)",
                                        "Mean Latency (ms)",
                                        "",
                                        y_scale='linear',
                                        x_min_factor=0.98,
                                        x_max_factor=1.02,
                                        y_min_factor=0.9,
                                        y_max_factor=1.05,
                                        xticks=data_xticks,
                                        xtick_labels=data_xtick_labels)

        self.plot_lines_with_error_bars(ax3,
                                        "99th Percentile Latency",
                                        "Flow Rate (Mbps)",
                                        "99th Percentile Latency (ms)",
                                        "",
                                        y_scale='linear',
                                        x_min_factor=0.98,
                                        x_max_factor=1.02,
                                        y_min_factor=0.9,
                                        y_max_factor=1.05,
                                        xticks=data_xticks,
                                        xtick_labels=data_xtick_labels)


        # xlabels = ax1.get_xticklabels()
        # plt.setp(xlabels, rotation=0, fontsize=8)

        xlabels = ax2.get_xticklabels()
        plt.setp(xlabels, rotation=0, fontsize=8)

        xlabels = ax3.get_xticklabels()
        plt.setp(xlabels, rotation=0, fontsize=8)

        # Shrink current axis's height by 25% on the bottom
        # box = ax1.get_position()
        # ax1.set_position([box.x0, box.y0 + box.height * 0.3,
        #                   box.width, box.height * 0.7])

        box = ax2.get_position()
        ax2.set_position([box.x0, box.y0 + box.height * 0.3, box.width, box.height * 0.7])

        box = ax3.get_position()
        ax3.set_position([box.x0, box.y0 + box.height * 0.3, box.width, box.height * 0.7])

        handles, labels = ax3.get_legend_handles_labels()

        ax2.legend(handles,
                   labels,
                   shadow=True,
                   fontsize=8,
                   loc='upper center',
                   ncol=2,
                   markerscale=1.0,
                   frameon=True,
                   fancybox=True,
                   columnspacing=0.7, bbox_to_anchor=[1.1, -0.25])

        plt.savefig("plots/" + self.experiment_tag + "_" + "qos_demo" + ".png", dpi=100)
        plt.show()

def prepare_flow_specifications(measurement_rates, tests_duration, same_queue_output):

    flow_specs = []

    flow_match = Match(is_wildcard=True)
    flow_match["ethernet_type"] = 0x0800
    # switch_hosts = ["h1s1", "h2s1", "h1s2", "h2s2"]
    #switch_hosts = ["h1s1", "h2s2"]
    switch_hosts = ["h1s1", "h1s2"]

    if same_queue_output:
        configured_rate = 100
    else:
        configured_rate = 50

    for src_host, dst_host in permutations(switch_hosts, 2):

        if src_host == dst_host:
            continue

        measurement_rates = []
        fs = FlowSpecification(src_host_id=src_host,
                               dst_host_id=dst_host,
                               configured_rate=configured_rate,
                               flow_match=flow_match,
                               measurement_rates=measurement_rates,
                               tests_duration=tests_duration,
                               delay_budget=None)

        flow_specs.append(fs)

    return flow_specs

def prepare_network_configurations(same_output_queue_list, measurement_rates,
                                   tests_duration):

    nc_list = []

    for same_output_queue in same_output_queue_list:
        flow_specs = prepare_flow_specifications(measurement_rates, tests_duration, same_output_queue)

        nc =  NetworkConfiguration("ryu_old",
                                  conf_root="configurations/",
                                  synthesis_name="SynthesizeQoS",
                                  synthesis_params={"same_output_queue": same_output_queue},
                                  flow_specs=flow_specs)

        nc_list.append(nc)

    return nc_list

def main():

    num_iterations = 1
    same_output_queue_list = [False, True]
    measurement_rates = [45, 46, 47, 48, 49, 50]
    nc_list = prepare_network_configurations(same_output_queue_list=same_output_queue_list,
                                             measurement_rates=measurement_rates,
                                             tests_duration=5)
    # flow_specs = prepare_flow_specifications()

    # network_configuration =  NetworkConfiguration("ryu_old",
    #                                   conf_root="configurations/",
    #                                   synthesis_name="SynthesizeQoS",
    #                                   synthesis_params={"same_output_queue": True},
    #                                   flow_specs=flow_specs)

    exp = QosDemo(nc_list, num_iterations, len(measurement_rates))

    exp.trigger()

if __name__ == "__main__":
    main()
