# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

from config import *
import helper_functions as hf
from collections import defaultdict
import numpy as np

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


def get_delay(result, delay_dict, tag_flow_prio):
    delay_list = []
    for n_flow_each_prio in result.N_FLOW_EACH_PRIO_LIST:
        delay_list.append(delay_dict[n_flow_each_prio][tag_flow_prio])

    return delay_list


def plot_single_node():

    # change font to Arial
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams['font.size'] = 15
    plt.rcParams['legend.fontsize'] = 13
    plt.rcParams['axes.titlesize'] = 15
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 10

    # filename = "../" + PARAMS.EXP_SINGLE_NODE_FILENAME
    filename = "exp_single_node_test1.pickle.gzip"
    result = hf.load_object_from_file(filename)

    all_delay_dict = result.all_delay_dict

    # i = 5
    # j = 4
    # k = 2
    #
    # print(all_delay_dict[i][j][k])

    # n_flow_each_prio = 2
    # tag_flow_prio = 4
    # dl = []
    #
    # for count in range(result.N_SINGLE_NODE_EXP_SAMPLE_RUN):
    #     dl.append(all_delay_dict[n_flow_each_prio][tag_flow_prio][count])
    #
    # print("Trace:", dl)

    mean_delay = defaultdict(lambda: defaultdict(dict))
    std_delay = defaultdict(lambda: defaultdict(dict))

    for n_flow_each_prio in result.N_FLOW_EACH_PRIO_LIST:
        for tag_flow_prio in result.TAG_FLOW_PRIO_LIST:
            dl = []
            for count in range(result.N_SINGLE_NODE_EXP_SAMPLE_RUN):
                dl.append(all_delay_dict[n_flow_each_prio][tag_flow_prio][count])

            print("Trace:", dl)
            mean_delay[n_flow_each_prio][tag_flow_prio] = np.mean(dl)/1000
            std_delay[n_flow_each_prio][tag_flow_prio] = np.std(dl)/1000


    print(mean_delay)

    print("mean:", mean_delay[5][4])
    print("std:", std_delay[5][4])


    y_pos = np.arange(len(result.N_FLOW_EACH_PRIO_LIST))
    y_delta = 0.25
    bar_width = 0.25

    tag_flow_prio = result.TAG_FLOW_PRIO_LIST[0]
    mean_delay_list = get_delay(result, mean_delay, tag_flow_prio)
    std_delay_list = get_delay(result, std_delay, tag_flow_prio)
    print(mean_delay_list)
    print(std_delay_list)
    plt.bar(y_pos, mean_delay_list, bar_width, yerr=std_delay_list,
            color=['gray'], edgecolor='k',
            alpha=0.7, label="Highest Priority (Level 0)")


    tag_flow_prio = result.TAG_FLOW_PRIO_LIST[1]
    mean_delay_list = get_delay(result, mean_delay, tag_flow_prio)
    std_delay_list = get_delay(result, std_delay, tag_flow_prio)
    print(mean_delay_list)
    print(std_delay_list)
    plt.bar(y_pos+y_delta, mean_delay_list,  bar_width, yerr=std_delay_list,
            color=['gray'],
            alpha=0.5,
            edgecolor='k',
            label="Medium Priority (Level 4)",
            error_kw=dict(ecolor='black', alpha=0.5, lw=2, capsize=5, capthick=2))

    tag_flow_prio = result.TAG_FLOW_PRIO_LIST[2]
    mean_delay_list = get_delay(result, mean_delay, tag_flow_prio)
    std_delay_list = get_delay(result, std_delay, tag_flow_prio)
    print(mean_delay_list)
    print(std_delay_list)
    plt.bar(y_pos + 2*y_delta, mean_delay_list, bar_width, yerr=std_delay_list,
            color=['gray'],
            alpha=0.3,
            edgecolor='k',
            label="Lowest Priority (Level 7)",
            error_kw=dict(ecolor='black', alpha=0.5, lw=2, capsize=5, capthick=2))

    plt.xticks(y_pos+bar_width, result.N_FLOW_EACH_PRIO_LIST)

    plt.xlabel('Number of Flows Each Queue')
    plt.ylabel('Mean Observed Delay (ms)')
    plt.legend()


    # plt.show()

    plt.tight_layout()

    plt.savefig("delay_validation.pdf")


if __name__ == '__main__':
    plot_single_node()