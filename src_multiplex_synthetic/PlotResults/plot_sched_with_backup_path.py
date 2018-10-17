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


from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
import copy


def cc(arg):
    return mcolors.to_rgba(arg, alpha=0.6)


def get_data_matrix(in_filename, EXP_NAME):

    result = hf.load_object_from_file(in_filename)

    N_FLOW_EACH_PRIO_LIST = result.N_FLOW_EACH_PRIO_LIST
    BASE_E2E_BETA_LIST = result.BASE_E2E_BETA_LIST
    SCHED_EXP_EACH_TRIAL_COUNT = result.SCHED_EXP_EACH_TRIAL_COUNT

    if EXP_NAME == 'PRIMARY':
        sched_count_dict = result.sched_count_dict_primary
    elif EXP_NAME == 'BKP_HP':
        sched_count_dict = result.sched_count_dict_bkp_hp
    elif EXP_NAME == 'BKP_ALL':
        sched_count_dict = result.sched_count_dict_bkp_all
    else:
        raise Exception("Invalid Experiment Name!")

    data = []
    for n in N_FLOW_EACH_PRIO_LIST:
        val = []
        for d in BASE_E2E_BETA_LIST:
            val.append((sched_count_dict[n][d] / SCHED_EXP_EACH_TRIAL_COUNT)*100)
            # val.append((sched_count_dict[n][d]))

        data.append(val)

    data = np.array(data)

    # print(data)
    return data


def get_x_values(in_filename,  nw_diameter=4):

    result = hf.load_object_from_file(in_filename)

    N_PRIO_LEVEL = result.N_PRIO_LEVEL
    N_FLOW_EACH_PRIO_LIST = result.N_FLOW_EACH_PRIO_LIST
    BASE_E2E_BETA_LIST = result.BASE_E2E_BETA_LIST

    x = [N_FLOW_EACH_PRIO_LIST[i] * N_PRIO_LEVEL for i in range(len(N_FLOW_EACH_PRIO_LIST))]
    delay_vals = [int(BASE_E2E_BETA_LIST[i]*1000*nw_diameter) for i in range(len(BASE_E2E_BETA_LIST))]  #convert to microsecond

    return x, delay_vals


def flat_list(org_list):
    flist = [item for sublist in org_list for item in sublist]
    return flist


def draw_plot(in_filename, out_filename):
    # change font to Arial
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams['font.size'] = 15
    plt.rcParams['legend.fontsize'] = 11
    plt.rcParams['axes.titlesize'] = 15
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 10

    data_matrix_primary = flat_list(get_data_matrix(in_filename=in_filename, EXP_NAME='PRIMARY').tolist())
    data_matrix_bkp_hp = flat_list(get_data_matrix(in_filename=in_filename, EXP_NAME='BKP_HP').tolist())
    data_matrix_bkp_all = flat_list(get_data_matrix(in_filename=in_filename, EXP_NAME='BKP_ALL').tolist())

    number_of_flows, _ = get_x_values(in_filename=in_filename)

    print("Org:", data_matrix_primary)
    print("Bkp_hp:", data_matrix_bkp_hp)
    print("Bkp_all:", data_matrix_bkp_all)

    n_groups = len(data_matrix_primary)

    index = np.arange(n_groups)
    bar_width = 0.35
    location_pad = 0.15
    opacity = 0.7

    # index = [int(i*2) for i in index]
    index = index * 2
    print("index:", index)

    plt.subplot(2, 1, 1)

    alpha = 0.9

    plt.bar(index, data_matrix_primary, bar_width,
            color=(0,0,0,0.8),
            edgecolor='k',
            label='Primary Path Only')

    plt.bar(index + bar_width, data_matrix_bkp_hp, bar_width,
            color=(0,0,0,0.4),
            edgecolor='k',
            hatch="",
            label='Primary and Backup Path (Only HP Flows)')

    plt.bar(index + 2*bar_width, data_matrix_bkp_all, bar_width,
            color=(0,0,0,0.05),
            edgecolor='k',
            hatch="",
            label='Primary and Backup Path (All Flows)')

    plt.xticks(index + 1.0 * bar_width, number_of_flows)

    plt.xlabel('Total Number of Flows')
    plt.ylabel('Acceptance Ratio (%)')

    plt.legend(ncol=1, loc='upper center', bbox_to_anchor=(0.5, 1.5))

    plt.savefig(out_filename, pad_inches=0.1, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    in_filename = "exp_sched_with_primary_backup_path_1000.pickle.gzip"


    draw_plot(in_filename=in_filename,
              out_filename='sched_backup_path.pdf')

    print("Script Finished!!")
