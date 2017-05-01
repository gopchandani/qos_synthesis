__author__ = 'Rakesh Kumar'

from collections import defaultdict
import threading
import paramiko
paramiko.util.log_to_file("filename.log")

import matplotlib.pyplot as plt
import sys

from experiment import Experiment
from network_configuration_hardware import NetworkConfiguration
from flow_specification import FlowSpecification
from model.match import Match

sys.path.append("./")
sys.path.append("../")


class QoSPica8Experiment(Experiment):

    def __init__(self,
                 network_configurations,
                 num_iterations,
                 num_measurements,
                 measurement_rates):

        super(QoSPica8Experiment, self).__init__("qos_pica8_experiment", 2)
        self.network_configurations = network_configurations
        self.controller_port = 6666
        self.num_iterations = num_iterations
        self.num_measurements = num_measurements
        self.measurement_rates = measurement_rates
        self.data = {
            "Throughput": defaultdict(defaultdict),
            "Mean Latency": defaultdict(defaultdict),
            "99th Percentile Latency": defaultdict(defaultdict),
            "Maximum Latency": defaultdict(defaultdict)
        }

    def trigger(self):
        for nc in self.network_configurations:
            self.clear_all_flows_queues()
            nc.setup_network_graph(mininet_setup_gap=1, synthesis_setup_gap=1)
            nc.init_flow_specs()
            nc.synthesis.synthesize_flow_specifications(nc.flow_specs)

            #self.push_arps(nc)
            self.measure_flow_rates(nc)

    def run_cmd_via_paramiko(self, IP, port, username, password, command):

        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.load_system_host_keys()
        s.connect(IP, port, username, password)
        (stdin, stdout, stderr) = s.exec_command(command)

        output = list(stdout.readlines())
        s.close()
        return output

    def clear_all_flows_queues(self):

        switches = [{"IP": "192.168.1.101",
                     "username": "admin",
                     "password": "password"},
                    {"IP": "192.168.1.103",
                     "username": "admin",
                     "password": "pica8"}
                    ]

        for sw in switches:
            self.run_cmd_via_paramiko(sw["IP"],
                                      22,
                                      sw["username"],
                                      sw["password"],
                                      "/ovs/bin/ovs-ofctl del-flows of-switch")

            self.run_cmd_via_paramiko(sw["IP"],
                                      22,
                                      sw["username"],
                                      sw["password"],
                                      "/ovs/bin/ovs-vsctl clear Port ge-1/1/43 qos")
            self.run_cmd_via_paramiko(sw["IP"],
                                      22,
                                      sw["username"],
                                      sw["password"],
                                      "/ovs/bin/ovs-vsctl clear Port ge-1/1/45 qos")
            self.run_cmd_via_paramiko(sw["IP"],
                                      22,
                                      sw["username"],
                                      sw["password"],
                                      "/ovs/bin/ovs-vsctl clear Port ge-1/1/47 qos")
            self.run_cmd_via_paramiko(sw["IP"],
                                      22,
                                      sw["username"],
                                      sw["password"],
                                      "/ovs/bin/ovs-vsctl --all destroy QoS")
            self.run_cmd_via_paramiko(sw["IP"],
                                      22,
                                      sw["username"],
                                      sw["password"],
                                      "/ovs/bin/ovs-vsctl --all destroy Queue")

    def push_arps(self, nc):

        # For each host in the topology,
        # send commands to add ARP entries for all other hosts

        for cmd_host_dict in nc.h_hosts.values():
            for other_host_dict in nc.h_hosts.values():

                if cmd_host_dict["host_name"] == other_host_dict["host_name"]:
                    continue

                arp_cmd = "sudo arp -s " + other_host_dict["host_IP"] + " " + other_host_dict["host_MAC"]

                print "Installing this at IP: %s" % cmd_host_dict["host_IP"]

                self.run_cmd_via_paramiko(cmd_host_dict["mgmt_ip"], 22,
                                          cmd_host_dict["usr"],
                                          cmd_host_dict["psswd"],
                                          arp_cmd)

            arp_cmd = "/usr/sbin/arp -n"

            self.run_cmd_via_paramiko(cmd_host_dict["mgmt_ip"], 22,
                                      cmd_host_dict["usr"],
                                      cmd_host_dict["psswd"],
                                      arp_cmd)

    def parse_measurements(self, data_lines):

        output_line_tokens = data_lines[2].split(',')

        measurements = dict()

        measurements["throughput"] = output_line_tokens[0]
        measurements["mean_latency"] = output_line_tokens[1]
        measurements["stdev_latency"] = output_line_tokens[2]
        measurements["nn_perc_latency"] = output_line_tokens[3]
        measurements["min_latency"] = output_line_tokens[4]
        measurements["max_latency"] = output_line_tokens[5]
        measurements["src_sent_packets"] = output_line_tokens[6]
        measurements["dst_recv_packets"] = output_line_tokens[7]

        return measurements

    def init_data(self, nc, clients, servers, measurement_rates):

        for client, server in zip(clients, servers):
            for rate in measurement_rates:
                if nc.synthesis_params["same_output_queue"]:
                    first_key = client["host_IP"] + "->" + server["host_IP"] + " Same output queue"
                else:
                    first_key = client["host_IP"] + "->" + server["host_IP"] + " Different output queue"

                second_key = rate

                self.data["Throughput"][first_key][second_key] = []
                self.data["Mean Latency"][first_key][second_key] = []
                self.data["99th Percentile Latency"][first_key][second_key] = []
                self.data["Maximum Latency"][first_key][second_key] = []

    def start_all_flows_simulatenously(self, nc, clients, servers, rate):
        client_threads = []

        for client, server in zip(clients, servers):
            netperf_cmd = nc.flow_specs[0].construct_netperf_cmd_str(rate, server["host_IP"])
            command = "%s | cat > /home/%s/out_%s.txt" \
                      % (netperf_cmd, client["usr"], str(rate))

            client_thread = threading.Thread(target=self.run_cmd_via_paramiko,
                                             args=(client["mgmt_ip"], 22, client["usr"], client["psswd"], command))
            client_thread.start()
            client_threads.append(client_thread)

        for client_thread in client_threads:
            client_thread.join()

    def collect_measurements(self, nc, clients, servers, rate):

        for client, server in zip(clients, servers):

            if nc.synthesis_params["same_output_queue"]:
                first_key = client["host_IP"] + "->" + server["host_IP"] + " Same output queue"
            else:
                first_key = client["host_IP"] + "->" + server["host_IP"] + " Different output queue"

            second_key = rate

            command = "cat /home/%s/out_%s.txt"  % (client["usr"], str(rate))
            output_lines = self.run_cmd_via_paramiko(client["mgmt_ip"], 22, client["usr"], client["psswd"],
                                                     command)

            measurements = self.parse_measurements(output_lines)

            self.data["Throughput"][first_key][second_key].append(float(measurements["throughput"]))
            self.data["Mean Latency"][first_key][second_key].append(float(measurements["mean_latency"]))
            self.data["99th Percentile Latency"][first_key][second_key].append(float(measurements["nn_perc_latency"]))
            self.data["Maximum Latency"][first_key][second_key].append(float(measurements["max_latency"]))

    def measure_flow_rates(self, nc):

        print "Using same output queues:", nc.synthesis_params["same_output_queue"]

        servers = [
            nc.h_hosts["66"],
            nc.h_hosts["7e"]
        ]
        # launch servers
        for serv in servers:
            command = "/usr/local/bin/netserver"
            self.run_cmd_via_paramiko(serv["mgmt_ip"], 22, serv["usr"], serv["psswd"], command)

        clients = [
            nc.h_hosts["e5"],
            nc.h_hosts["38"]
        ]

        self.init_data(nc, clients, servers, self.measurement_rates)

        for i in range(self.num_iterations):
            print "iteration:", i + 1

            for rate in self.measurement_rates:
                print "Send Rate:", rate
                self.start_all_flows_simulatenously(nc, clients, servers, rate)
                self.collect_measurements(nc, clients, servers, rate)

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


def prepare_flow_specifications(measurement_rates=None, tests_duration=None, same_queue_output=False):

    flow_specs = []

    flow_match = Match(is_wildcard=True)
    flow_match["ethernet_type"] = 0x0800
    switch_hosts = ["7e", "e5", "66", "38"]

    configured_rate = 50

    # for src_host, dst_host in permutations(switch_hosts, 2):
    for src_host, dst_host in [("7e", "38"),
                               ("38", "7e"),
                               ("66", "e5"),
                               ("e5", "66")]:
        if src_host == dst_host:
            continue

        # measurement_rates = []
        fs = FlowSpecification(src_host_id=src_host,
                               dst_host_id=dst_host,
                               configured_rate=configured_rate,
                               flow_match=flow_match,
                               measurement_rates=measurement_rates,
                               tests_duration=tests_duration,
                               delay_budget=None)

        flow_specs.append(fs)

    return flow_specs


def prepare_network_configurations(same_output_queue_list,
                                   measurement_rates,
                                   tests_duration):

    nc_list = []

    for same_output_queue in same_output_queue_list:
        flow_specs = prepare_flow_specifications(measurement_rates, tests_duration, same_output_queue)

        nc = NetworkConfiguration("ryu_old",
                                  conf_root="configurations/",
                                  synthesis_name="SynthesizeQoS",
                                  synthesis_params={"same_output_queue": same_output_queue},
                                  flow_specs=flow_specs)

        nc_list.append(nc)

    return nc_list


def main():

    num_iterations = 30
    same_output_queue_list = [False, True]
    measurement_rates = [42, 45, 50]
    nc_list = prepare_network_configurations(same_output_queue_list=same_output_queue_list,
                                             measurement_rates=measurement_rates,
                                             tests_duration=15)

    exp = QoSPica8Experiment(nc_list, num_iterations, len(measurement_rates), measurement_rates)
    exp.trigger()
    exp.dump_data()
    exp.plot_qos()

    print exp.data

if __name__ == "__main__":
    main()
