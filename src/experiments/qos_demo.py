__author__ = 'Rakesh Kumar'

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
                 flow_duration,
                 flow_rates,
                 network_configurations):

        super(QosDemo, self).__init__("number_of_hosts", num_iterations)
        self.flow_duration = flow_duration
        self.flow_rates = flow_rates
        self.network_configurations = network_configurations
        self.flow_measurements = []

        self.cm = ControllerMan(controller="ryu")
        self.cm.stop_controller()
        time.sleep(5)
        self.controller_port = self.cm.start_controller()

        self.data = {
            "Throughput": defaultdict(defaultdict),
            "99th Percentile Latency": defaultdict(defaultdict),
            "Maximum Latency": defaultdict(defaultdict)
        }

    def populate_data(self):
        for nc in self.network_configurations:
            print "network_configuration:", nc

            for i in range(len(self.flow_rates)):

                self.data["Throughput"][nc.topo_params["num_hosts_per_switch"]][self.flow_rates[i]] = []
                self.data["99th Percentile Latency"][nc.topo_params["num_hosts_per_switch"]][self.flow_rates[i]] = []
                self.data["Maximum Latency"][nc.topo_params["num_hosts_per_switch"]][self.flow_rates[i]] = []

        print self.data

    def plot_data(self):
        pass

    def trigger(self):

        for i in range(self.num_iterations):

            print "iteration:", i + 1

            for nc in self.network_configurations:
                print "network_configuration:", nc

                nc.setup_network_graph(mininet_setup_gap=1, synthesis_setup_gap=1)

                flow_specifications = []
                for src, dst in nc.ng.host_obj_pair_iter():
                    if src == dst:
                        continue

                    flow_match = Match(is_wildcard=True)
                    flow_match["ethernet_type"] = 0x0800

                    if src.node_id == "h11" and dst.node_id == "h21":
                        flow_specifications.append(FlowSpecification(src, dst, 1, flow_match))
                    if src.node_id == "h21" and dst.node_id == "h11":
                        flow_specifications.append(FlowSpecification(src, dst, 1, flow_match))
                    if src.node_id == "h12" and dst.node_id == "h22":
                        flow_specifications.append(FlowSpecification(src, dst, 150, flow_match))
                    if src.node_id == "h22" and dst.node_id == "h12":
                        flow_specifications.append(FlowSpecification(src, dst, 150, flow_match))

                nc.synthesis.synthesize_flow_specifications(flow_specifications)
                self.flow_measurements.append(self.measure_flow_rates(nc))

    def parse_iperf_output(self, iperf_output_string):
        data_lines =  iperf_output_string.split('\r\n')
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
        data_tokens =  data_lines[interesting_line_index].split()
        data_tokens =  data_tokens[3].split('/')
        print 'Min Delay:', data_tokens[0]
        print 'Avg Delay:', data_tokens[1]
        print 'Max Delay:', data_tokens[2]

    def measure_flow_rates(self, nc):

        # Get all the nodes
        h11 = nc.mininet_obj.getNodeByName("h11")
        h21 = nc.mininet_obj.getNodeByName("h21")
        h12 = nc.mininet_obj.getNodeByName("h12")
        h22 = nc.mininet_obj.getNodeByName("h22")

        h1s1_output = h11.cmd("/usr/local/bin/netserver")
        print h1s1_output

        h2s1_output = h12.cmd("/usr/local/bin/netserver")
        print h2s1_output

        # Initialize flow measurements
        h1s2_to_h1s1_flow_measurements = []
        h2s2_to_h2s1_flow_measurements = []

        flow_1_rate = [0.1, 0.1, 0.1, 0.1]
        flow_2_rate = [10, 40, 60, 80]

        for i in range(len(self.flow_rates)):# in self.flow_rates:

            flow_match = Match(is_wildcard=True)
            flow_match["ethernet_type"] = 0x0800

            h1s2_to_h1s1_flow_measurement = FlowSpecification(h21, h11, flow_1_rate[i], flow_match)
            h2s2_to_h2s1_flow_measurement = FlowSpecification(h22, h12, flow_2_rate[i], flow_match)

            h21.cmd(h1s2_to_h1s1_flow_measurement.construct_netperf_cmd_str(self.flow_duration))
            h22.cmd(h2s2_to_h2s1_flow_measurement.construct_netperf_cmd_str(self.flow_duration))

            # Sleep for 5 seconds more than flow duration to make sure netperf has finished.
            time.sleep(self.flow_duration + 10)

            h1s2_to_h1s1_flow_measurement.parse_netperf_output(h21.read())
            h2s2_to_h2s1_flow_measurement.parse_netperf_output(h22.read())

            h1s2_to_h1s1_flow_measurements.append(h1s2_to_h1s1_flow_measurement)
            h2s2_to_h2s1_flow_measurements.append(h2s2_to_h2s1_flow_measurement)

            print h1s2_to_h1s1_flow_measurement
            print h2s2_to_h2s1_flow_measurement

        return h1s2_to_h1s1_flow_measurements, h2s2_to_h2s1_flow_measurements


def prepare_network_configurations(num_hosts_per_switch_list, same_output_queue_list):
    nc_list = []

    for same_output_queue in same_output_queue_list:

        for hps in num_hosts_per_switch_list:

            nc = NetworkConfiguration("ryu",
                                      "linear_modified",
                                      {"num_switches": 2,
                                       "num_hosts_per_switch": hps},
                                      conf_root="configurations/",
                                      synthesis_name="SynthesizeQoS",
                                      synthesis_params={"same_output_queue": same_output_queue})

            nc_list.append(nc)

    return nc_list


def main():

    num_iterations = 2
    flow_duration = 15
    flow_rates = [40, 45, 50, 55]#, 60]
    num_hosts_per_switch_list = [2]
    same_output_queue_list = [True]#[False, True]
    network_configurations = prepare_network_configurations(num_hosts_per_switch_list, same_output_queue_list)

    exp = QosDemo(num_iterations, flow_duration, flow_rates, network_configurations)

    exp.trigger()
    exp.populate_data()
    exp.plot_data()

if __name__ == "__main__":
    main()