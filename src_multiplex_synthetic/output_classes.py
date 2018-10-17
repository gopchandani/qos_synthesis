# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

import copy

class ExportSingleNodeDelay:

    """ A Class to format single node output result """

    def __init__(self, N_FLOW_EACH_PRIO_LIST, TAG_FLOW_PRIO_LIST, N_SINGLE_NODE_EXP_SAMPLE_RUN, all_delay_dict):
        self.N_FLOW_EACH_PRIO_LIST = copy.deepcopy(N_FLOW_EACH_PRIO_LIST)
        self.TAG_FLOW_PRIO_LIST = copy.deepcopy(TAG_FLOW_PRIO_LIST)
        self.N_SINGLE_NODE_EXP_SAMPLE_RUN = N_SINGLE_NODE_EXP_SAMPLE_RUN
        self.all_delay_dict = copy.deepcopy(all_delay_dict)


class ExportSchedResult:
    """ A Class to format schedulability output result """

    def __init__(self, NUMBER_OF_SWITCHES, NUM_HOST_PER_SWITCH,
                 N_PRIO_LEVEL, N_FLOW_EACH_PRIO_LIST, BASE_E2E_BETA_LIST,
                 SCHED_EXP_EACH_TRIAL_COUNT, sched_count_dict):

        self.NUMBER_OF_SWITCHES = NUMBER_OF_SWITCHES
        self.NUM_HOST_PER_SWITCH = NUM_HOST_PER_SWITCH
        self.N_PRIO_LEVEL = N_PRIO_LEVEL
        self.N_FLOW_EACH_PRIO_LIST = copy.deepcopy(N_FLOW_EACH_PRIO_LIST)
        self.BASE_E2E_BETA_LIST = copy.deepcopy(BASE_E2E_BETA_LIST)
        self.SCHED_EXP_EACH_TRIAL_COUNT = SCHED_EXP_EACH_TRIAL_COUNT
        self.sched_count_dict = copy.deepcopy(sched_count_dict)


class ExportForwardBackupPathSchedResult:
    """ A Class to format schedulability output result with backup path """

    def __init__(self, NUMBER_OF_SWITCHES, NUM_HOST_PER_SWITCH,
                 N_PRIO_LEVEL, N_FLOW_EACH_PRIO_LIST, BASE_E2E_BETA_LIST,
                 SCHED_EXP_EACH_TRIAL_COUNT,
                 sched_count_dict_primary,
                 sched_count_dict_bkp_hp,
                 sched_count_dict_bkp_all):

        self.NUMBER_OF_SWITCHES = NUMBER_OF_SWITCHES
        self.NUM_HOST_PER_SWITCH = NUM_HOST_PER_SWITCH
        self.N_PRIO_LEVEL = N_PRIO_LEVEL
        self.N_FLOW_EACH_PRIO_LIST = copy.deepcopy(N_FLOW_EACH_PRIO_LIST)
        self.BASE_E2E_BETA_LIST = copy.deepcopy(BASE_E2E_BETA_LIST)
        self.SCHED_EXP_EACH_TRIAL_COUNT = SCHED_EXP_EACH_TRIAL_COUNT
        self.sched_count_dict_primary = copy.deepcopy(sched_count_dict_primary)
        self.sched_count_dict_bkp_hp = copy.deepcopy(sched_count_dict_bkp_hp)
        self.sched_count_dict_bkp_all = copy.deepcopy(sched_count_dict_bkp_all)
