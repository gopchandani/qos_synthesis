
class FlowSpecification:
    def __init__(self, src_host_id, dst_host_id, configured_rate, flow_match, measurement_rates, tests_duration):
        self.src_host_id = src_host_id
        self.dst_host_id = dst_host_id
        self.configured_rate = configured_rate
        self.flow_match = flow_match

        self.measurement_rates = measurement_rates
        self.tests_duration = tests_duration
        self.measurements = []

        self.ng_src_host = None
        self.ng_dst_host = None

        self.mn_src_host = None
        self.mn_dst_host = None

        self.num_sends_in_burst = 10
        self.inter_burst_time = 1

        self.send_size = configured_rate * 1000 / (8 * self.num_sends_in_burst)
        self.configured_rate_bps = self.send_size * 8 * self.num_sends_in_burst * 1000

    def construct_netperf_cmd_str(self, measurement_rate):

        # netperf input parameters

        # measurement_rate is given in Mbps (Mega bits per second, fixing inter_burst_time to 1 (ms) and
        # num_sends_in_burst to 10 for this calculation and using this equation
        # measurement_rate * 10^6 = (num_sends_in_burst * send_size * 8) / (1 * 10^-3)
        # so: send_size = measurement_rate * 10^3 / (8 * num_sends_in_burst)

        self.send_size = measurement_rate * 1000 / (8 * self.num_sends_in_burst)
        self.measurement_rate_bps = self.send_size * 8 * self.num_sends_in_burst * 1000

        netperf_cmd_str = "/usr/local/bin/netperf -H " + self.mn_dst_host.IP() + \
                          " -w " + str(self.inter_burst_time) + \
                          " -b " + str(self.num_sends_in_burst) + \
                          " -l " + str(self.tests_duration) + \
                          " -t omni -- -d send" + \
                          " -o " + \
                          "'THROUGHPUT, MEAN_LATENCY, STDDEV_LATENCY, P99_LATENCY, MIN_LATENCY, MAX_LATENCY'" + \
                          " -T UDP_RR " + \
                          "-m " + str(self.send_size) + " &"

        return netperf_cmd_str

    def store_measurements(self, netperf_output_string):

        data_lines = netperf_output_string.split('\r\n')
        output_line_tokens = data_lines[2].split(',')

        self.throughput = output_line_tokens[0]
        self.mean_latency = output_line_tokens[1]
        self.stdev_latency = output_line_tokens[2]
        self.nn_perc_latency = output_line_tokens[3]
        self.min_latency = output_line_tokens[4]
        self.max_latency = output_line_tokens[5]

    def __str__(self):
        return "Send Rate: " + str(self.configured_rate/1000000.0) + \
               " src_host_id: " + str(self.src_host_id) + \
               " dst_host_id: " + str(self.dst_host_id)
