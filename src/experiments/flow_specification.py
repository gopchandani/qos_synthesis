
class FlowSpecification:
    def __init__(self, src_host, dst_host, send_rate):
        self.src_host = src_host
        self.dst_host = dst_host
        self.send_rate = send_rate

        # netperf input parameters

        # send_rate is given in Mbps (Mega bits per second, fixing inter_burst_time to 1 (ms) and
        # num_sends_in_burst to 10 for this calculation and using this equation

        # send_rate * 10^6 = (num_sends_in_burst * send_size * 8) / (1 * 10^-3)

        # so: send_size = send_rate * 10^3 / (8 * num_sends_in_burst)

        self.num_sends_in_burst = 10
        self.inter_burst_time = 1
        self.send_size = send_rate * 1000 / (8 * self.num_sends_in_burst)

        self.send_rate_bps = self.send_size * 8 * self.num_sends_in_burst * 1000

        self.netperf_cmd_str = None

        # netperf output variables
        self.throughput = None
        self.mean_latency = None
        self.stdev_latency = None
        self.nn_perc_latency = None
        self.min_latency = None
        self.max_latency = None

    def construct_netperf_cmd_str(self):
        self.netperf_cmd_str = "/usr/local/bin/netperf -H " + self.dst_host.IP() + \
                               " -w " + str(self.inter_burst_time) + \
                               " -b " + str(self.num_sends_in_burst) + \
                               " -l 10 " + \
                               "-t omni -- -d send" + \
                               " -o " + \
                               "'THROUGHPUT, MEAN_LATENCY, STDDEV_LATENCY, P99_LATENCY, MIN_LATENCY, MAX_LATENCY'" + \
                               " -T UDP_RR " + \
                               "-m " + str(self.send_size) + " &"

        return self.netperf_cmd_str

    def parse_netperf_output(self, netperf_output_string):

        data_lines = netperf_output_string.split('\r\n')
        output_line_tokens = data_lines[2].split(',')

        self.throughput = output_line_tokens[0]
        self.mean_latency = output_line_tokens[1]
        self.stdev_latency = output_line_tokens[2]
        self.nn_perc_latency = output_line_tokens[3]
        self.min_latency = output_line_tokens[4]
        self.max_latency = output_line_tokens[5]

    def __str__(self):
        return "Send Rate: " + str(self.send_rate) + \
               " Throughput: " + str(self.throughput) + \
               " 99th Percentile Latency: " + str(self.nn_perc_latency)
