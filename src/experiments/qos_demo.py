__author__ = 'Rakesh Kumar'

import sys
import time

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

            nc.setup_network_graph(mininet_setup_gap=1, synthesis_setup_gap=1)
            self.measure_flow_rates(nc, nc.synthesis_params["global_flow_rate"])

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

        data_lines =  ping_output_string.split('\r\n')
        interesting_line_index = None
        for i in xrange(len(data_lines)):
            if data_lines[i].startswith('5 packets transmitted'):
                interesting_line_index = i + 1
        data_tokens =  data_lines[interesting_line_index].split()
        data_tokens =  data_tokens[3].split('/')
        print 'Min Delay:', data_tokens[0]
        print 'Avg Delay:', data_tokens[1]
        print 'Max Delay:', data_tokens[2]

    def parse_netperf_output(self,netperf_output_string):
        data_lines =  netperf_output_string.split('\r\n')

        output_line_tokens =  data_lines[2].split(',')
        print "Throughput:", output_line_tokens[0]
        print 'Mean Latency:', output_line_tokens[1]
        print 'Stddev Latency:', output_line_tokens[2]
        print '99th Latency:', output_line_tokens[3]
        print 'Min Latency:', output_line_tokens[4]
        print 'Max Latency:', output_line_tokens[5]

    def measure_flow_rates(self, nc, last_hop_queue_rate):

        num_traffic_profiles = 10
        size_of_send = [1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024]

        number_of_sends_in_a_burst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        inter_burst_times = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        # Get all the nodes
        self.h1s1 = nc.mininet_obj.getNodeByName("h1s1")
        self.h1s2 = nc.mininet_obj.getNodeByName("h1s2")
        self.h2s1 = nc.mininet_obj.getNodeByName("h2s1")
        self.h2s2 = nc.mininet_obj.getNodeByName("h2s2")

        h1s1_output = self.h1s1.cmd("/usr/local/bin/netserver")
        print h1s1_output

        h2s1_output = self.h2s1.cmd("/usr/local/bin/netserver")
        print h2s1_output

        netperf_output_dict_h1s2 = {}
        netperf_output_dict_h2s2 = {}

        for i in range(num_traffic_profiles):

            netperf_output_dict_h1s2[i] = self.h1s2.cmd("/usr/local/bin/netperf -H " + self.h1s1.IP() +
                                                        " -w " + str(inter_burst_times[i]) +
                                                        " -b " + str(number_of_sends_in_a_burst[i]) +
                                                        " -l 10 " +
                                                        "-t omni -- -d send -o " +
                                                        "'THROUGHPUT, MEAN_LATENCY, STDDEV_LATENCY, P99_LATENCY, MIN_LATENCY, MAX_LATENCY'" +
                                                        " -T UDP_RR " +
                                                        "-m " + str(size_of_send[i]) + " &"
                                                        )

            netperf_output_dict_h2s2[i] = self.h2s2.cmd("/usr/local/bin/netperf -H " + self.h2s1.IP() +
                                                        " -w " + str(inter_burst_times[i]) +
                                                        " -b " + str(number_of_sends_in_a_burst[i]) +
                                                        " -l 10 " +
                                                        "-t omni -- -d send -o " +
                                                        "'THROUGHPUT, MEAN_LATENCY, STDDEV_LATENCY, P99_LATENCY, MIN_LATENCY, MAX_LATENCY'" +
                                                        " -T UDP_RR " +
                                                        "-m " + str(size_of_send[i]) + " &"
                                                        )
            time.sleep(15)

            netperf_output_dict_h1s2[i] = self.h1s2.read()
            netperf_output_dict_h2s2[i] = self.h2s2.read()

            print netperf_output_dict_h1s2[i]
            print netperf_output_dict_h2s2[i]

        # Parse the output for jitter and delay
        print "Last-Hop Queue Rate:", str(last_hop_queue_rate), "M"
        for i in range(num_traffic_profiles):

            print "--"
            print "Size of send (bytes):", size_of_send[i]
            print "Number of sends in a burst:", number_of_sends_in_a_burst[i]
            print "Inter-burst time (miliseconds):", inter_burst_times[i]

            rate = (size_of_send[i] * 8 * number_of_sends_in_a_burst[i]) / (inter_burst_times[i] * 1000.0)
            print "Sending Rate:", str(rate), 'Mbps'

            self.parse_netperf_output(netperf_output_dict_h1s2[i])
            print "--"
            self.parse_netperf_output(netperf_output_dict_h2s2[i])


def prepare_network_configurations(num_hosts_per_switch_list, global_flow_rate_list, same_output_queue_list):
    nc_list = []

    for same_output_queue in same_output_queue_list:
        for global_flow_rate in global_flow_rate_list:

            for hps in num_hosts_per_switch_list:

                nc = NetworkConfiguration("ryu",
                                          "linear",
                                          {"num_switches": 2,
                                           "num_hosts_per_switch": hps},
                                          conf_root="configurations/",
                                          synthesis_name="SynthesizeQoS",
                                          synthesis_params={"global_flow_rate": global_flow_rate,
                                                            "same_output_queue": same_output_queue})

                nc_list.append(nc)

    return nc_list


def main():

    num_iterations = 1
    num_hosts_per_switch_list = [2]#[2, 4, 6, 8, 10]
    global_flow_rate_list = [50]
    same_output_queue_list = [False, True]
    network_configurations = prepare_network_configurations(num_hosts_per_switch_list,
                                                            global_flow_rate_list,
                                                            same_output_queue_list)

    exp = QosDemo(num_iterations, network_configurations)

    exp.trigger()

if __name__ == "__main__":
    main()