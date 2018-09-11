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

    """
    SOME STATS
        
    for 50 Kbyte packet size minimum BW req (10 is the min period): (50*1000*8)/10
    
    [8, 800] for 1 Kbit packet size
    [40, 4000] for 5 Kb
    [80, 8000] for 10Kbit packet size
    [120, 12000] 15Kb
    [200, 20000] for 25 Kb
    [400, 40000] 50 Kb
    
    max bw req in a link for 30 flows with 10 Kbyte packet size
    [80, 8000] * 30 = [2.4, 240] Mbps
    
    max bw req in a link for 30 flows with 50 Kbyte packet size
    [400, 40000] * 30 = [12, 1200] Mbps
    
    for 1024 Byte packet
    BW req for [10, 1000] ms flow: [(1024*8)/(10), (1024*8)/(1000)] = [0.8192, 0.008192] Mbits
     

    """

    NUMBER_OF_SWITCHES = 5
    NUM_HOST_PER_SWITCH = 2

    # propagation delay ranges (in millisecond)
    # ((1024*8)/(10 * 1000 * 1000)) * 1000 = 0.8192 millisecond
    PROP_DELAY_MIN = 0.8192 + 0.000505  # 505 nanosecond propagation delay, 0.8192 transmission delay
    PROP_DELAY_MAX = 0.8192 + 0.000505

    LINK_BW = 10 * 1000  # link capacity in kbps

    # period range (in millisecond)
    PERIOD_MIN = 10
    PERIOD_MAX = 1000

    DELAY_DELTA = 10  # how much e2e deadline we vary from flow to flow (function of base_e2e_delta and NW diameter)
    BASE_E2E_BETA_LIST = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]  # see RTSS paper, how we set E2E deadline based on Topology (diamaeter of NW)

    N_PRIO_LEVEL = 3  # number of priority levels

    # this two variable must be in same length
    PKT_SIZE_LIST = [256 * 8, 1408 * 8]  # size of the packets (in bits)
    PKT_PROCESSING_TIME_LIST = [8.548/1000, 22.54/1000]  # corresponding processing time (in millisecond)

    MAX_LOOP_COUNT = 10000  # just an upperbound of loop iteration

    LARGE_NUMBER = 100000  # a large number
    # PARAMS for single node experiment

    N_FLOW_EACH_PRIO_LIST = [1, 3, 5, 7, 9, 11]  # for single node experiment
    N_FLOW_EACH_PRIO_LIST_SCHED = [1, 3, 5, 7, 9, 11]  # number of each flow in each queue for schedualbility experiment

    TAG_FLOW_PRIO_LIST = [0, 1, 2]  # HI, MED, LO

    N_SINGLE_NODE_EXP_SAMPLE_RUN = 10000  # number of sample runs for single node experiment

    SCHED_EXP_EACH_TRIAL_COUNT = 50  # number of trials for schedulability experiment

    EXP_SINGLE_NODE_FILENAME = 'exp_single_node.pickle.gzip'
    EXP_SCHED_FILENAME = 'exp_sched.pickle.gzip'