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

    NUMBER_OF_SWITCHES = 8
    NUM_HOST_PER_SWITCH = 2

    # propagation delay ranges (in microseconds)
    PROP_DELAY_MIN = 5
    PROP_DELAY_MAX = 25

    LINK_BW = 10 * 1000  # link capacity in kbps

    # period range (in millisecond)
    PERIOD_MIN = 10
    PERIOD_MAX = 1000

    N_PRIO_LEVEL = 3  # number of priority levels

    # this two variable must be in same length
    PKT_SIZE_LIST = [400*8, 512*8, 1024*8]  # size of the packets (in bits)
    PKT_PROCESSING_TIME_LIST = [25/1000, 25/1000, 25/1000]  # corresponding processing time (in millisecond)


    # BASE_UTIL = 0.9  # base utilization per switch

    MAX_LOOP_COUNT = 1000  # just an upperbound of loop iteration

    LARGE_NUMBER = 100000  # a large number
    # PARAMS for single node experiment

    N_FLOW_EACH_PRIO_LIST = [2, 5, 10, 20, 50]
    TAG_FLOW_PRIO_LIST = [0, 4, 7]

    N_SINGLE_NODE_EXP_SAMPLE_RUN = 100  # number of sample runs

    EXP_SINGLE_NODE_FILENAME = 'exp_single_node.pickle.gzip'

