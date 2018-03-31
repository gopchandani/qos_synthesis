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




def plot_sched(filename):

    # change font to Arial
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams['font.size'] = 15
    plt.rcParams['legend.fontsize'] = 13
    plt.rcParams['axes.titlesize'] = 15
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 10

    result = hf.load_object_from_file(filename)


    NUMBER_OF_SWITCHES = result.NUMBER_OF_SWITCHES
    NUM_HOST_PER_SWITCH = result.NUM_HOST_PER_SWITCH
    N_PRIO_LEVEL = result.N_PRIO_LEVEL
    N_FLOW_EACH_PRIO_LIST = result.N_FLOW_EACH_PRIO_LIST
    BASE_E2E_BETA_LIST = result.BASE_E2E_BETA_LIST
    SCHED_EXP_EACH_TRIAL_COUNT = result.SCHED_EXP_EACH_TRIAL_COUNT
    sched_count_dict = result.sched_count_dict

    BASE_E2E_BETA_LIST.reverse()  # for test

    data = []
    for n in N_FLOW_EACH_PRIO_LIST:
        val = []
        for d in BASE_E2E_BETA_LIST:
            val.append(sched_count_dict[n][d]/SCHED_EXP_EACH_TRIAL_COUNT)

        data.append(val)

    data = np.array(data)

    print(data)

    N_PRIO_LEVEL = 3

    column_names = BASE_E2E_BETA_LIST
    row_names = [N_FLOW_EACH_PRIO_LIST[i] * N_PRIO_LEVEL for i in range(len(N_FLOW_EACH_PRIO_LIST))]

    print("NFLOW EACH PRIo", N_FLOW_EACH_PRIO_LIST)
    print("N_PRIO_LEV", N_PRIO_LEVEL)
    print("Row name:", row_names)

    # column_names = ['a', 'b', 'c', 'd', 'e']
    # row_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    fig = plt.figure()
    ax = Axes3D(fig)

    """
    lx = len(data[0])  # Work out matrix dimensions
    ly = len(data[:, 0])
    xpos = np.arange(0, lx, 1)  # Set up a mesh of positions
    ypos = np.arange(0, ly, 1)
    xpos, ypos = np.meshgrid(xpos + 0.25, ypos + 0.25)

    xpos = xpos.flatten()  # Convert positions to 1D array
    ypos = ypos.flatten()
    zpos = np.zeros(lx * ly)

    dx = 0.5 * np.ones_like(zpos)
    dy = dx.copy()
    dz = data.flatten()

    # cs = ['r', 'g', 'b', 'y', 'c'] * ly
    # cs = ['#DCDCDC', '#D3D3D3', '#C0C0C0', '#A9A9A9', '#808080'] * ly
    # print("color:", cs)

    cs = plt.cm.gray(data.flatten() / float(data.max()))
    # print("color:", cs)

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=cs, edgecolor='k', alpha=0.7)
    # ax.bar3d(xpos, ypos, zpos, dx, dy, dz)

    # sh()
    ax.w_xaxis.set_ticklabels(column_names)
    ax.w_yaxis.set_ticklabels(row_names)
    ax.set_xlabel('End To End Deadline')
    ax.set_ylabel('Total Number of Flows')
    ax.set_zlabel('Acceptance Ratio (%)')

    # ax.view_init(azim=50, elev=15)
    ax.view_init(azim=-67, elev=15)

    ticksx = np.arange(0.5, len(column_names), 1)
    plt.xticks(ticksx, column_names)

    ticksy = np.arange(0.6, len(row_names), 1)
    plt.yticks(ticksy, row_names)

    plt.show()
    """

    X, Y = np.meshgrid(N_FLOW_EACH_PRIO_LIST, BASE_E2E_BETA_LIST)

    # Z = np.zeros((len(N_FLOW_EACH_PRIO_LIST), (len(BASE_E2E_BETA_LIST)))  # initialize

    Z = np.zeros((len(BASE_E2E_BETA_LIST), len(N_FLOW_EACH_PRIO_LIST)))  # initialize

    #
    # for row in range(len(N_FLOW_EACH_PRIO_LIST)):
    #     for col in range(len(BASE_E2E_BETA_LIST)):
    #         vv = sched_count_dict[N_FLOW_EACH_PRIO_LIST[row]][BASE_E2E_BETA_LIST[col]]
    #         Z[row][col] = vv/SCHED_EXP_EACH_TRIAL_COUNT

    for row in range(len(BASE_E2E_BETA_LIST)):
        for col in range(len(N_FLOW_EACH_PRIO_LIST)):
            vv = sched_count_dict[N_FLOW_EACH_PRIO_LIST[col]][BASE_E2E_BETA_LIST[row]]
            Z[row][col] = vv/SCHED_EXP_EACH_TRIAL_COUNT

    print("X:", X)
    print("Y:", Y)
    print("Z:", Z)
    # ax.plot_surface(X, Y, Z, linewidth=2.0, cmap=plt.cm.Blues, rstride=1, cstride=1, alpha=0.4)
    ax.plot_surface(X, Y, Z)

    plt.show()


if __name__ == '__main__':
    filename = "exp_sched.pickle.gzip"
    plot_sched(filename)

    print("Script Finished!!")
