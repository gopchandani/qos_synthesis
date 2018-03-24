# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"


class ExportSingleNodeDelay:

    """ A Class to format single node output result """

    def __init__(self, N_FLOW_EACH_PRIO_LIST, TAG_FLOW_PRIO_LIST, N_SINGLE_NODE_EXP_SAMPLE_RUN, all_delay_dict):
        self.N_FLOW_EACH_PRIO_LIST = N_FLOW_EACH_PRIO_LIST
        self.TAG_FLOW_PRIO_LIST = TAG_FLOW_PRIO_LIST
        self.N_SINGLE_NODE_EXP_SAMPLE_RUN = N_SINGLE_NODE_EXP_SAMPLE_RUN
        self.all_delay_dict = all_delay_dict
