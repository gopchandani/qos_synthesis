__author__ = 'Rakesh Kumar'

import matplotlib.pyplot as plt
import sys
import time
from collections import defaultdict

sys.path.append("./")

from controller_man import ControllerMan
from experiment import Experiment
from network_configuration import NetworkConfiguration
from flow_specification import FlowSpecification
from model.match import Match


class QosDemo(Experiment):

    def __init__(self,
                 num_iterations,
                 network_configurations,
                 num_measurements):

        super(QosDemo, self).__init__("qos_demo", num_iterations)
        self.network_configurations = network_configurations
        self.num_measurements = num_measurements

        self.cm = ControllerMan(controller="ryu")
        self.cm.stop_controller()
        time.sleep(5)
        self.controller_port = self.cm.start_controller()

    def prepare_data(self):

        self.data = {
            "Throughput": defaultdict(defaultdict),
            "Mean Latency": defaultdict(defaultdict),
            "99th Percentile Latency": defaultdict(defaultdict),
            "Maximum Latency": defaultdict(defaultdict)
        }

        for nc in self.network_configurations:

            for fs in nc.flow_specs:

                if not fs.measurement_rates:
                    continue

                for measurement_rate in fs.measurement_rates:

                    first_key = fs.src_host_id + "->" + fs.dst_host_id +\
                                " same_output_queue = " + str(nc.synthesis_params["same_output_queue"])

                    second_key = measurement_rate

                    self.data["Throughput"][first_key][second_key] = []
                    self.data["Mean Latency"][first_key][second_key] = []
                    self.data["99th Percentile Latency"][first_key][second_key] = []
                    self.data["Maximum Latency"][first_key][second_key] = []

        for nc in self.network_configurations:

            for fs in nc.flow_specs:

                if not fs.measurement_rates:
                    continue

                for measurement_rate in fs.measurement_rates:

                    first_key = fs.src_host_id + "->" + fs.dst_host_id +\
                                " same_output_queue = " + str(nc.synthesis_params["same_output_queue"])

                    second_key = measurement_rate

                    for measurement in fs.measurements[measurement_rate]:
                        self.data["Throughput"][first_key][second_key].append(float(measurement["throughput"]))
                        self.data["Mean Latency"][first_key][second_key].append(float(measurement["mean_latency"]))
                        self.data["99th Percentile Latency"][first_key][second_key].append(float(measurement["nn_perc_latency"]))
                        self.data["Maximum Latency"][first_key][second_key].append(float(measurement["max_latency"]))


    def plot_qos(self):

        f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=False, sharey=False, figsize=(9.5, 3.0))

        data_xticks = self.network_configurations[0].flow_specs[0].measurement_rates
        data_xtick_labels = [str(x) for x in data_xticks]

        self.plot_lines_with_error_bars(ax1,
                                        "Throughput",
                                        "",
                                        "Throughput(Mbps)",
                                        "(a)",
                                        y_scale='linear',
                                        x_min_factor=0.95,
                                        x_max_factor=1.05,
                                        y_min_factor=0.01,
                                        y_max_factor=1,
                                        xticks=data_xticks,
                                        xtick_labels=data_xtick_labels)

        ax1.set_ylim(40, 47.5)

        self.plot_lines_with_error_bars(ax2,
                                        "Mean Latency",
                                        "Flow Rate",
                                        "Mean Latency(ms)",
                                        "(b)",
                                        y_scale='linear',
                                        x_min_factor=0.95,
                                        x_max_factor=1.05,
                                        y_min_factor=0.1,
                                        y_max_factor=1.2,
                                        xticks=data_xticks,
                                        xtick_labels=data_xtick_labels)

        self.plot_lines_with_error_bars(ax3,
                                        "99th Percentile Latency",
                                        "",
                                        "99th Percentile Latency(ms)",
                                        "(c)",
                                        y_scale='linear',
                                        x_min_factor=0.95,
                                        x_max_factor=1.05,
                                        y_min_factor=0.01,
                                        y_max_factor=1,
                                        xticks=data_xticks,
                                        xtick_labels=data_xtick_labels)


        xlabels = ax1.get_xticklabels()
        plt.setp(xlabels, rotation=0, fontsize=8)

        xlabels = ax2.get_xticklabels()
        plt.setp(xlabels, rotation=0, fontsize=8)

        xlabels = ax3.get_xticklabels()
        plt.setp(xlabels, rotation=0, fontsize=8)

        # Shrink current axis's height by 25% on the bottom
        box = ax1.get_position()
        ax1.set_position([box.x0, box.y0 + box.height * 0.3,
                          box.width, box.height * 0.7])

        box = ax2.get_position()
        ax2.set_position([box.x0, box.y0 + box.height * 0.3,
                          box.width, box.height * 0.7])

        box = ax3.get_position()
        ax3.set_position([box.x0, box.y0 + box.height * 0.3,
                          box.width, box.height * 0.7])

        handles, labels = ax3.get_legend_handles_labels()

        ax1.legend(handles,
                   labels,
                   shadow=True,
                   fontsize=8,
                   loc='upper center',
                   ncol=2,
                   markerscale=1.0,
                   frameon=True,
                   fancybox=True,
                   columnspacing=0.5, bbox_to_anchor=[1.6, -0.27])

        plt.savefig("plots/" + self.experiment_tag + "_" + "qos_demo" + ".png", dpi=100)
        plt.show()

    def trigger(self):

        for nc in self.network_configurations:
            print "network_configuration:", nc

            nc.setup_network_graph(mininet_setup_gap=1, synthesis_setup_gap=1)
            nc.init_flow_specs()
            nc.synthesis.synthesize_flow_specifications(nc.flow_specs)
            self.measure_flow_rates(nc)

    def parse_iperf_output(self, iperf_output_string):
        data_lines = iperf_output_string.split('\r\n')
        interesting_line_index = None
        for i in xrange(len(data_lines)):
             if data_lines[i].endswith('Server Report:'):
                interesting_line_index = i + 1
        data_tokens =  data_lines[interesting_line_index].split()
        print "Transferred Rate:", data_tokens[7]
        print "Jitter:", data_tokens[9]

    def parse_ping_output(self,ping_output_string):

        data_lines = ping_output_string.split('\r\n')
        interesting_line_index = None
        for i in xrange(len(data_lines)):
            if data_lines[i].startswith('5 packets transmitted'):
                interesting_line_index = i + 1
        data_tokens = data_lines[interesting_line_index].split()
        data_tokens = data_tokens[3].split('/')
        print 'Min Delay:', data_tokens[0]
        print 'Avg Delay:', data_tokens[1]
        print 'Max Delay:', data_tokens[2]

    def measure_flow_rates(self, nc):

        for i in range(self.num_iterations):
            print "iteration:", i + 1

            for j in range(self.num_measurements):

                max_fs_duration = 0

                for fs in nc.flow_specs:

                    if not fs.measurement_rates:
                        continue

                    server_output = fs.mn_dst_host.cmd("/usr/local/bin/netserver")
                    client_output = fs.mn_src_host.cmd(fs.construct_netperf_cmd_str(fs.measurement_rates[j]))

                    if fs.tests_duration > max_fs_duration:
                        max_fs_duration = fs.tests_duration

                # Sleep for 5 seconds more than flow duration to make sure netperf has finished.
                time.sleep(max_fs_duration + 5)

                for fs in nc.flow_specs:

                    if not fs.measurement_rates:
                        continue

                    fs.measurements[fs.measurement_rates[j]].append(fs.parse_measurements(fs.mn_src_host.read()))


def prepare_network_configurations(same_output_queue_list, measurement_rates, tests_duration):
    nc_list = []

    for same_output_queue in same_output_queue_list:

        flow_specs = prepare_flow_specifications(measurement_rates, tests_duration)

        nc = NetworkConfiguration("ryu",
                                  "linear",
                                  {"num_switches": 2,
                                   "num_hosts_per_switch": 2},
                                  conf_root="configurations/",
                                  synthesis_name="SynthesizeQoS",
                                  synthesis_params={"same_output_queue": same_output_queue},
                                  flow_specs=flow_specs)

        nc_list.append(nc)

    return nc_list


def prepare_flow_specifications(measurement_rates, tests_duration):

    flow_specs = []

    flow_match = Match(is_wildcard=True)
    flow_match["ethernet_type"] = 0x0800

    h1s2_to_h1s1 = FlowSpecification("h1s2", "h1s1", 50, flow_match, measurement_rates, tests_duration)
    h2s2_to_h2s1 = FlowSpecification("h2s2", "h2s1", 50, flow_match, measurement_rates, tests_duration)

    h1s1_to_h1s2 = FlowSpecification("h1s1", "h1s2", 50, flow_match, [], tests_duration)
    h2s1_to_h2s2 = FlowSpecification("h2s1", "h2s2", 50, flow_match, [], tests_duration)

    flow_specs.append(h1s2_to_h1s1)
    flow_specs.append(h2s2_to_h2s1)

    flow_specs.append(h1s1_to_h1s2)
    flow_specs.append(h2s1_to_h2s2)

    return flow_specs


def main():

    num_iterations = 25
    tests_duration = 10

    measurement_rates = [45, 46, 47, 48, 49, 50]
    same_output_queue_list = [False, True]
    network_configurations = prepare_network_configurations(same_output_queue_list,
                                                            measurement_rates,
                                                            tests_duration)

    exp = QosDemo(num_iterations, network_configurations, len(measurement_rates))

    # exp.trigger()
    # exp.prepare_data()
    # exp.dump_data()

    exp.load_data("data/qos_demo_25_iterations_20161001_202626.json")

    exp.plot_qos()

if __name__ == "__main__":
    main()
