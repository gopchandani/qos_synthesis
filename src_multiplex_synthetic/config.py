# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

""" Helper for creating constant variables
    Found in: https://stackoverflow.com/questions/2682745/how-to-create-a-constant-in-python
"""

class MetaConst(type):
    def __getattr__(cls, key):
        return cls[key]

    def __setattr__(cls, key, value):
        raise TypeError


class Const(object, metaclass=MetaConst):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        raise TypeError


class PARAMS(Const):

    """ This class stores all the configuration parameters """

    NUMBER_OF_SWITCHES = 5
    NUM_HOST_PER_SWITCH = 1

    # propagation delay ranges (in microseconds)
    PROP_DELAY_MIN = 5
    PROP_DELAY_MAX = 25

    # DELAY_DELTA = 5/1000  # how much e2e deadline difference from flow i to flow i+1 (in second)
    # BASE_DELAY_BUDGET_PAD = 0.1  # the base delay budget padding (on top of nw diameter) [in percentage]

    LINK_BW = 10  # link capacity in bps

    # packet size range (in bits)
    PKT_SIZE_MIN = 25 * 8
    PKT_SIZE_MAX = 125 * 8

    # period range (in microsecond)
    PERIOD_MIN = 10*1000
    PERIOD_MAX = 1000*1000

    N_PRIO_LEVEL = 8  # number of priority levels

    PCKT_PROCESSING_TIME = 25  # in microsecond (obtained from our Ashish experiments)

    # BASE_UTIL = 0.9  # base utilization per switch

    MAX_LOOP_COUNT = 1000  # just an upperbound of loop iteration

    # PARAMS for single node experiment

    N_FLOW_EACH_PRIO_LIST = [2, 5, 10, 20, 50]
    # N_FLOW_EACH_PRIO_LIST = [2, 5]
    TAG_FLOW_PRIO_LIST = [0, 4, 7]

    N_SINGLE_NODE_EXP_SAMPLE_RUN = 1000  # number of sample runs

    EXP_SINGLE_NODE_FILENAME = 'exp_single_node.pickle.gzip'

