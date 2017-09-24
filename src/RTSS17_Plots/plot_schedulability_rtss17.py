import matplotlib
matplotlib.use('TkAgg')

import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import pickle


def get_back_objects(filename):

    # Getting back the objects:
    with open(filename) as f:
        number_of_RT_flow_list, number_of_test_cases, base_delay_budget_list, shed_count, minimum_diameter = pickle.load(
            f)

    return number_of_RT_flow_list, number_of_test_cases, base_delay_budget_list, shed_count, minimum_diameter


def plot_acceptance_ratio(filename, fignum=1):

    # fig = plt.figure(fignum, figsize=(10, 6))
    fig = plt.figure(fignum)

    plt.hold(True)



    number_of_RT_flow_list, number_of_test_cases, base_delay_budget_list, shed_count, minimum_diameter = get_back_objects(
        filename)

    # base_delay_budget_list[3] = 0.000100

    # number_of_RT_flow_list.remove(8)
    # number_of_RT_flow_list.remove(7)
    # number_of_RT_flow_list.remove(6)

    print "=== begin budget list ==="
    print base_delay_budget_list
    print "=== end budget list ==="
    n = len(base_delay_budget_list)
    base_delay_budget_list.pop(n-1)
    # base_delay_budget_list.pop(n-2)
    base_delay_budget_list.pop(0)
    base_delay_budget_list.pop(0)
    # base_delay_budget_list.pop(0)
    # base_delay_budget_list.pop(0)
    # base_delay_budget_list.pop(0)
    # base_delay_budget_list.pop(0)

    print "delay-budget length:{}".format(len(base_delay_budget_list))
    print "#flow length:{}".format(len(number_of_RT_flow_list))

    # make it int
    number_of_RT_flow_list = [int(x) for x in number_of_RT_flow_list]

    X, Y = np.meshgrid(base_delay_budget_list, number_of_RT_flow_list)

    X = np.multiply(X, minimum_diameter)
    X = np.multiply(X, 1000000)  # convert to us

    # Z = np.zeros((len(base_delay_budget_list), len(number_of_RT_flow_list))) # initialize
    Z = np.zeros((len(number_of_RT_flow_list), len(base_delay_budget_list)))  # initialize

    print X
    print "base delay"
    print base_delay_budget_list
    print 'printing y'
    print Y

    print shed_count

    sum = 1

    for row in range(len(number_of_RT_flow_list)):
        # sum = 1
        for col in range(len(base_delay_budget_list)):
            # print number_of_RT_flow_list[col]
            Z[row][col] = shed_count[number_of_RT_flow_list[row]][base_delay_budget_list[col]]
            # Z[row][col] = sum
            sum += 1

            print "#of flow: {}, delay: {}, Z: {}".format(number_of_RT_flow_list[row], base_delay_budget_list[col], Z[row][col])

    #Z = X + Y
    print X
    print Y
    print Z

    Z = np.multiply(Z, 100.00/number_of_test_cases)

    print Z

    # print base_delay_budget_list

    ax = fig.add_subplot(111, projection='3d')
    # ax.plot_surface(X, Y, Z)
    # ax.plot_wireframe(X, Y, Z)



    ax.plot_surface(X, Y, Z, linewidth=1.0, cmap=cm.Blues, rstride=1, cstride=1, alpha = 0.4)




    ax.set_xlabel('Delay Requirement ($\mu$s)', fontsize=15)
    ax.set_ylabel('Number of Flows', fontsize=15)
    ax.set_zlabel('Acceptance Ratio (%)', fontsize=15)

    ax.tick_params(axis='both', labelsize=11)

    # ax.view_init(elev=40.0, azim=-135)
    # ax.view_init(elev=27.0, azim=-156)
    # ax.view_init(elev=20.0, azim=101)
    ax.view_init(elev=23.0, azim=-137)

    plt.yticks(np.arange(min(number_of_RT_flow_list), max(number_of_RT_flow_list)+1, 1.0))

    # ax.grid(False)
    for a in (ax.w_xaxis, ax.w_yaxis, ax.w_zaxis):
        # for t in a.get_ticklines() + a.get_ticklabels():
            # t.set_visible(False)
        # a.line.set_visible(False)
        a.pane.set_visible(False)

    # fig.set_tight_layout(True)

    plt.tight_layout()
    plt.savefig('schedulability.pdf', pad_inches=-0.1, bbox_inches='tight')
    # plt.savefig('schedulability.pdf')

    plt.show()


if __name__ == "__main__":
    filename = 'shedulability_traces.pickle'
    plot_acceptance_ratio(filename, fignum=1)



