class FlowMeasurement:
    def __init__(self, src_host, dst_host, send_rate):
        self.src_host = src_host
        self.dst_host = dst_host
        self.send_rate = send_rate

        # netperf input parameters
        self.send_size = 1024
        self.num_sends_in_burst = 10
        self.inter_burst_time = 1
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
        return "Send Rate:" + str(self.send_rate) + \
               " Throughput:" + str(self.throughput) + \
               " 99th Percentile Latency:" + str(self.nn_perc_latency)
