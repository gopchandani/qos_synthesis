from collections import defaultdict


class FlowSpecification:
    def __init__(self, src_host_id, dst_host_id, configured_rate,
                 flow_match, measurement_rates, tests_duration,
                 # mhasan: added delay field
                 delay_budget):
        self.src_host_id = src_host_id
        self.dst_host_id = dst_host_id
        self.configured_rate = configured_rate
        self.flow_match = flow_match

        self.measurement_rates = measurement_rates
        self.tests_duration = tests_duration

        # Store per_rate, list of measurements, each representing a list containing values per iteration
        self.measurements = defaultdict(list)

        self.ng_src_host = None
        self.ng_dst_host = None

        self.mn_src_host = None
        self.mn_dst_host = None

        self.num_sends_in_burst = 10
        self.inter_burst_time = 1

        # self.send_size = configured_rate * 1e6 / (8 * self.num_sends_in_burst)
        self.configured_rate_bps = configured_rate * 1e6

        self.measurement_rate_bps = None

        # mhasan: added delay field
        self.delay_budget = delay_budget  # end to end delay requirement
        # mhasan: added Path
        self.path = None

    def construct_netperf_cmd_str(self, measurement_rate, ip=""):

        # netperf input parameters

        # measurement_rate is given in Mbps (Mega bits per second, fixing inter_burst_time to 1 (ms) and
        # num_sends_in_burst to 10 for this calculation and using this equation
        # measurement_rate * 10^6 = (num_sends_in_burst * send_size * 8) / (1 * 10^-3)
        # so: send_size = measurement_rate * 10^3 / (8 * num_sends_in_burst)

        self.send_size = measurement_rate * 1e6 / (8 * self.num_sends_in_burst * 100)
        self.measurement_rate_bps = self.send_size * 8 * self.num_sends_in_burst * 1000

        netperf_cmd_str = "/usr/local/bin/netperf -H " + ip + \
                          " -w " + str(self.inter_burst_time) + \
                          " -b " + str(self.num_sends_in_burst) + \
                          " -l " + str(self.tests_duration) + \
                          " -t omni -- -d send" + \
                          " -o " + \
                          "\"THROUGHPUT, MEAN_LATENCY, STDDEV_LATENCY, P99_LATENCY, MIN_LATENCY, MAX_LATENCY, LOCAL_BYTES_SENT, REMOTE_BYTES_RECVD\"" + \
                          " -T UDP_RR " + \
                          "-m " + str(self.send_size)

        # netperf_cmd_str = "/usr/local/bin/netperf " + \
        #                   " -j " + \
        #                   " -H " + self.mn_dst_host.IP() + \
        #                   " -t UDP_RR " + \
        #                   " -l " + str(self.tests_duration) + \
        #                   " -t omni -- -d send" + \
        #                   " -o " + \
        #                   "'THROUGHPUT, MEAN_LATENCY, STDDEV_LATENCY, P99_LATENCY, MIN_LATENCY, MAX_LATENCY'" + \
        #                   " -m " + str(self.send_size) + \
        #                   " &"

        return netperf_cmd_str

    def parse_measurements(self, netperf_output_string):

        data_lines = netperf_output_string.split('\n')
        output_line_tokens = data_lines[2].split(',')

        measurements = dict()

        measurements["throughput"] = output_line_tokens[0]
        measurements["mean_latency"] = output_line_tokens[1]
        measurements["stdev_latency"] = output_line_tokens[2]
        measurements["nn_perc_latency"] = output_line_tokens[3]
        measurements["min_latency"] = output_line_tokens[4]
        measurements["max_latency"] = output_line_tokens[5]

        return measurements

    def get_null_measurement(self):

        measurements = dict()

        measurements["throughput"] = "-1"
        measurements["mean_latency"] = "-1"
        measurements["stdev_latency"] = "-1"
        measurements["nn_perc_latency"] = "-1"
        measurements["min_latency"] = "-1"
        measurements["max_latency"] = "-1"

        return measurements

    def __str__(self):
        return "Send Rate: " + str(self.configured_rate/1000000.0) + \
               " src_host_id: " + str(self.src_host_id) + \
               " dst_host_id: " + str(self.dst_host_id)
