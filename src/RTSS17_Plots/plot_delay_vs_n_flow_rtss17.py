import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import statsmodels.api as sm # recommended import according to the docs
import matplotlib.pyplot as plt
import pickle


def get_back_objects(filename):

    # Getting back the objects:
    with open(filename) as f:
        number_of_RT_flow_list, number_of_BE_flow_list, number_of_test_cases, measurement_rates, delay_budget, output_data_list = pickle.load(f)

    return number_of_RT_flow_list, number_of_BE_flow_list, number_of_test_cases, measurement_rates, delay_budget, output_data_list


def get_data_for_delay_throughput(number_of_RT_flow_list, output_data_list, n_BE_flows, info):

    exp_data = []  # 2D list : row : # of flows, col: experimental samples

    for nf in range(len(number_of_RT_flow_list)):
        exp_data.append([])
        for i, dd in enumerate(output_data_list):
            if dd['number_of_RT_flows'] == number_of_RT_flow_list[nf] and dd['number_of_BE_flows'] == n_BE_flows:
                if info == "mean_latency":
                    exp_data[nf].append(dd['max_mean_latency'])

                elif info == "max_latency":
                    exp_data[nf].append(dd['max_max_latency'])

                elif info == "nn_latency":
                    exp_data[nf].append(dd['max_nn_latency'])

                elif info == "throughput":
                    exp_data[nf].append(dd['min_throughput'])

                elif info == "max_possible_delay_e2e":
                    exp_data[nf].append(dd['max_possible_delay_e2e'])

                elif info == "max_delay_budget_e2e":
                    exp_data[nf].append(dd['max_delay_budget_e2e'])

                elif info == "min_delay_budget_e2e":
                    exp_data[nf].append(dd['min_delay_budget_e2e'])

                elif info == "max_bw_req":
                    exp_data[nf].append(dd['max_bw_req'])

                elif info == "required_bw":
                    exp_data[nf].append(dd['measurement_rates'])

                else:
                    raise NotImplementedError
    return exp_data


def extract_data_for_all_flow_list(number_of_flow_list, output_data_list, n_BE_flows):

    exp_data_mean = get_data_for_delay_throughput(number_of_flow_list, output_data_list, n_BE_flows, "mean_latency")
    exp_data_nn = get_data_for_delay_throughput(number_of_flow_list, output_data_list, n_BE_flows, "nn_latency")
    exp_data_max = get_data_for_delay_throughput(number_of_flow_list, output_data_list, n_BE_flows, "max_latency")
    exp_data_throughput = get_data_for_delay_throughput(number_of_flow_list, output_data_list, n_BE_flows, "throughput")
    exp_data_max_possible_e2e_delay = get_data_for_delay_throughput(number_of_flow_list, output_data_list, n_BE_flows,
                                                                    "max_possible_delay_e2e")
    exp_data_max_delay_budget_e2e = get_data_for_delay_throughput(number_of_flow_list, output_data_list, n_BE_flows,
                                                                  "max_delay_budget_e2e")
    exp_data_min_delay_budget_e2e = get_data_for_delay_throughput(number_of_flow_list, output_data_list, n_BE_flows,
                                                                  "min_delay_budget_e2e")
    exp_data_max_bw_req = get_data_for_delay_throughput(number_of_flow_list, output_data_list, n_BE_flows, "max_bw_req")
    exp_data_req_bw = get_data_for_delay_throughput(number_of_flow_list, output_data_list, n_BE_flows, "required_bw")

    # return (exp_data_mean, exp_data_nn, exp_data_max, exp_data_throughput,
    #         exp_data_max_possible_e2e_delay, exp_data_max_delay_budget_e2e, exp_data_min_delay_budget_e2e,
    #         exp_data_max_bw_req, exp_data_req_bw)

    return {'exp_data_mean': exp_data_mean,
            'exp_data_nn': exp_data_nn,
            'exp_data_max': exp_data_max,
            'exp_data_throughput': exp_data_throughput,
            'exp_data_max_possible_e2e_delay': exp_data_max_possible_e2e_delay,
            'exp_data_max_delay_budget_e2e': exp_data_max_delay_budget_e2e,
            'exp_data_min_delay_budget_e2e': exp_data_min_delay_budget_e2e,
            'exp_data_max_bw_req': exp_data_max_bw_req,
            'exp_data_req_bw': exp_data_req_bw}



def compute_ecdf(sample, type):

    # first check if there is any invalid entry
    sample = [x for x in sample if x != -1]

    # sample = np.array(map(float, sample))
    if type == "delay":
        # sample[:] = [x / 1000.00 for x in sample]  # changing unit to microsecond to ms (and divide by 2 for RTT?)
        sample[:] = [x / 1.00 for x in sample]
    elif type == "throughput":
        sample[:] = [x / 1.00 for x in sample]  # MBPS
    else:
        raise NotImplementedError

    ecdf = sm.distributions.ECDF(sample)
    x = np.linspace(min(sample), max(sample))
    y = ecdf(x)

    return x, y


def plot_without_be_flows(filename, fignum=1):
    fig = plt.figure(fignum)

    common_xlim = 40

    plt.hold(True)

    alpha = 1

    number_of_RT_flow_list, number_of_BE_flow_list, number_of_test_cases, measurement_rates, delay_budget, output_data_list = get_back_objects(
        filename)

    n_BE_flows = number_of_BE_flow_list[1]  # index one means no BE flows

    all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, n_BE_flows)

    exp_data_mean = all_value_dict['exp_data_mean']
    exp_data_nn = all_value_dict['exp_data_nn']
    exp_data_max = all_value_dict['exp_data_max']
    exp_data_throughput = all_value_dict['exp_data_throughput']
    exp_data_max_possible_e2e_delay = all_value_dict['exp_data_max_possible_e2e_delay']
    exp_data_max_delay_budget_e2e = all_value_dict['exp_data_max_delay_budget_e2e']
    exp_data_min_delay_budget_e2e = all_value_dict['exp_data_min_delay_budget_e2e']
    exp_data_max_bw_req = all_value_dict['exp_data_max_bw_req']
    exp_data_req_bw = all_value_dict['exp_data_req_bw']

    plt.subplot(2, 2, 1)

    flow_index = number_of_RT_flow_list.index(2)
    x, y = compute_ecdf(exp_data_mean[flow_index], "delay")
    plt.plot(x, y, alpha=alpha, color="k", marker="+", markerfacecolor="None", label='Mean Delay')

    flow_index = number_of_RT_flow_list.index(2)
    x, y = compute_ecdf(exp_data_nn[flow_index], "delay")
    plt.plot(x, y, alpha=alpha, color="k", marker=".", markerfacecolor="None", label='99th Percentile Delay')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('Delay ($\mu$s)', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    plt.title('2 Flows')
    plt.gca().set_xlim([0, common_xlim])

    plt.subplot(2, 2, 3)

    flow_index = number_of_RT_flow_list.index(3)
    x, y = compute_ecdf(exp_data_mean[flow_index], "delay")
    plt.plot(x, y, alpha=alpha, color="k", marker="+", markerfacecolor="None", label='4 Flows (Mean)')

    flow_index = number_of_RT_flow_list.index(3)
    x, y = compute_ecdf(exp_data_nn[flow_index], "delay")
    plt.plot(x, y, alpha=alpha, color="k", marker=".", markerfacecolor="None", label='4 Flows (99th Percentile)')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('Delay ($\mu$s)', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    plt.title('3 Flows')
    plt.gca().set_xlim([0, common_xlim])

    plt.subplot(2, 2, 2)

    flow_index = number_of_RT_flow_list.index(4)
    x, y = compute_ecdf(exp_data_mean[flow_index], "delay")
    plt.plot(x, y, alpha=alpha, color="k", marker="+", markerfacecolor="None", label='4 Flows (Mean)')

    flow_index = number_of_RT_flow_list.index(4)
    x, y = compute_ecdf(exp_data_nn[flow_index], "delay")
    plt.plot(x, y, alpha=alpha, color="k", marker=".", markerfacecolor="None", label='4 Flows (99th Percentile)')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('Delay ($\mu$s)', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    plt.title('4 Flows')
    plt.gca().set_xlim([0, common_xlim])

    plt.subplot(2, 2, 4)

    flow_index = number_of_RT_flow_list.index(5)
    x, y = compute_ecdf(exp_data_mean[flow_index], "delay")
    plt.plot(x, y, alpha=alpha, color="k", marker="+", markerfacecolor="None", label='Mean Delay')

    flow_index = number_of_RT_flow_list.index(5)
    x, y = compute_ecdf(exp_data_nn[flow_index], "delay")
    plt.plot(x, y, alpha=alpha, color="k", marker=".", markerfacecolor="None", label='99th Percentile Delay')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('Delay ($\mu$s)', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    plt.title('5 Flows')
    plt.gca().set_xlim([0, common_xlim])

    axes = plt.gca()
    lgd = axes.legend(loc='upper center', bbox_to_anchor=(-0.15, -0.25),
                      ncol=2)

    fig.set_tight_layout(True)
    #fig.savefig('mhasan_mean_nn_delay.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')  # No warning now



    plt.show()


def plot_mean_delay_with_be_flows(filename, fignum=1):

    fig = plt.figure(fignum)
    # common_xlim = 10

    plt.hold(True)

    alpha = 0.6

    number_of_RT_flow_list, number_of_BE_flow_list, number_of_test_cases, measurement_rates, delay_budget, output_data_list = get_back_objects(
        filename)

    n_BE_flows = number_of_BE_flow_list[0]  # index one means no BE flows


    all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, n_BE_flows)

    exp_data_mean_w_be = all_value_dict['exp_data_mean']
    exp_data_nn_w_be = all_value_dict['exp_data_nn']

    # all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, 0)  # 0 means no BE flows
    #
    # exp_data_mean_wo_be = all_value_dict['exp_data_mean']
    # exp_data_nn_wo_be = all_value_dict['exp_data_nn']

    plt.subplot(2, 1, 1)
    # Average
    flow_index = number_of_RT_flow_list.index(2)
    x, y = compute_ecdf(exp_data_mean_w_be[flow_index], "delay")
    plt.plot(x, y, linestyle='--', alpha=alpha, color="b", marker="+", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='2 Flows')

    flow_index = number_of_RT_flow_list.index(5)
    x, y = compute_ecdf(exp_data_mean_w_be[flow_index], "delay")
    plt.plot(x, y, linestyle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='5 Flows')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('Mean Delay ($\mu$s)', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    # plt.gca().set_xlim([0, common_xlim])

    plt.gca().legend(loc='lower right')

    fig.set_tight_layout(True)
    fig.savefig('delay_mean.pdf', bbox_inches='tight')

    plt.show()



def plot_99p_delay_with_be_flows(filename, fignum=1):

    fig = plt.figure(fignum)
    common_xlim = 40

    plt.hold(True)

    alpha = 0.6

    number_of_RT_flow_list, number_of_BE_flow_list, number_of_test_cases, measurement_rates, delay_budget, output_data_list = get_back_objects(
        filename)

    n_BE_flows = number_of_BE_flow_list[0]  # index one means no BE flows


    all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, n_BE_flows)

    exp_data_mean_w_be = all_value_dict['exp_data_mean']
    exp_data_nn_w_be = all_value_dict['exp_data_nn']

    # all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, 0)  # 0 means no BE flows
    #
    # exp_data_mean_wo_be = all_value_dict['exp_data_mean']
    # exp_data_nn_wo_be = all_value_dict['exp_data_nn']

    plt.subplot(2, 1, 1)

    # 99th percentile
    flow_index = number_of_RT_flow_list.index(2)
    x, y = compute_ecdf(exp_data_nn_w_be[flow_index], "delay")
    plt.plot(x, y, linestyle='--', alpha=alpha, color="b", marker="+", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='2 Flows')

    flow_index = number_of_RT_flow_list.index(5)
    x, y = compute_ecdf(exp_data_nn_w_be[flow_index], "delay")
    plt.plot(x, y, linestyle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='5 Flows')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('99th Percentile Delay ($\mu$s)', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    plt.gca().set_xlim([0, common_xlim])

    plt.gca().legend(loc='lower right')

    fig.set_tight_layout(True)
    fig.savefig('delay_99p.pdf', bbox_inches='tight')

    plt.show()


def plot_max_delay_with_be_flows(filename, fignum=1):

    fig = plt.figure(fignum)
    # common_xlim = 1200

    plt.hold(True)

    alpha = 0.6

    number_of_RT_flow_list, number_of_BE_flow_list, number_of_test_cases, measurement_rates, delay_budget, output_data_list = get_back_objects(
        filename)

    n_BE_flows = number_of_BE_flow_list[0]  # index one means no BE flows


    all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, n_BE_flows)

    exp_data_mean_w_be = all_value_dict['exp_data_mean']
    exp_data_nn_w_be = all_value_dict['exp_data_nn']
    exp_data_max_w_be = all_value_dict['exp_data_max']

    plt.subplot(2, 1, 1)

    # max delay
    # flow_index = number_of_RT_flow_list.index(2)
    # x, y = compute_ecdf(exp_data_max_w_be[flow_index], "delay")
    # plt.plot(x, y, linestyle='--', alpha=alpha, color="b", marker="+", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='2 Flows')

    flow_index = number_of_RT_flow_list.index(6)
    x, y = compute_ecdf(exp_data_max_w_be[flow_index], "delay")
    plt.plot(x, y, linestyle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='Worst-case Delay')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('End-to-End Delay ($\mu$s)', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    # plt.gca().set_xlim([0, common_xlim])

    plt.gca().legend(loc='lower right')

    fig.set_tight_layout(True)
    fig.savefig('delay_max.pdf', bbox_inches='tight')

    plt.show()



def plot_mean_and_99p_delay_with_be_flows(filename, fignum=1):

    fig = plt.figure(fignum)
    # common_xlim = 40

    plt.hold(True)

    alpha = 0.6

    number_of_RT_flow_list, number_of_BE_flow_list, number_of_test_cases, measurement_rates, delay_budget, output_data_list = get_back_objects(
        filename)

    n_BE_flows = number_of_BE_flow_list[0]  # index one means no BE flows


    all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, n_BE_flows)

    exp_data_mean_w_be = all_value_dict['exp_data_mean']
    exp_data_nn_w_be = all_value_dict['exp_data_nn']
    # exp_data_max_w_be = all_value_dict['exp_data_max']

    # all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, 0)  # 0 means no BE flows
    #
    # exp_data_mean_wo_be = all_value_dict['exp_data_mean']
    # exp_data_nn_wo_be = all_value_dict['exp_data_nn']

    plt.subplot(2, 1, 1)
    # Average
    flow_index = number_of_RT_flow_list.index(6)
    x, y = compute_ecdf(exp_data_mean_w_be[flow_index], "delay")
    plt.plot(x, y, linestyle='--', alpha=alpha, color="b", marker="+", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='Mean Delay')

    # flow_index = number_of_RT_flow_list.index(6)
    # x, y = compute_ecdf(exp_data_mean_w_be[flow_index], "delay")
    # plt.plot(x, y, linestyle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='5 Flows')

    # plt.ylabel('Empirical CDF', fontsize=15)
    # plt.xlabel('Mean Delay ($\mu$s)', fontsize=15)
    # plt.tick_params(axis='both', labelsize=12)
    # plt.gca().set_xlim([0, common_xlim])
    #
    # plt.gca().legend(loc='lower right')

    # fig.set_tight_layout(True)





    # fig.set_tight_layout(True)

    # plt.subplot(2, 1, 2)

    # 99th percentile
    # flow_index = number_of_RT_flow_list.index(2)
    # x, y = compute_ecdf(exp_data_nn_w_be[flow_index], "delay")
    # plt.plot(x, y, linestyle='--', alpha=alpha, color="b", marker="+", markerfacecolor="None", markersize=8,
    #          markeredgewidth=1.5, linewidth=2, label='2 Flows')

    flow_index = number_of_RT_flow_list.index(6)
    x, y = compute_ecdf(exp_data_nn_w_be[flow_index], "delay")
    plt.plot(x, y, linestyle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8,
             markeredgewidth=1.5, linewidth=2, label='99th Percentile Delay')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('End-to-End Delay ($\mu$s)', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    # plt.gca().set_xlim([0, common_xlim])

    plt.gca().legend(loc='lower right')

    # fig.set_tight_layout(True)
    fig.savefig('delay_mean_99p.pdf', bbox_inches='tight')

    plt.show()



def plot_mean_and_99p_and_max_delay_with_be_flows(filename, fignum=1):

    fig = plt.figure(fignum)
    common_xlim = 40

    plt.hold(True)

    alpha = 0.6

    number_of_RT_flow_list, number_of_BE_flow_list, number_of_test_cases, measurement_rates, delay_budget, output_data_list = get_back_objects(
        filename)

    n_BE_flows = number_of_BE_flow_list[0]  # index one means no BE flows


    all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, n_BE_flows)

    exp_data_mean_w_be = all_value_dict['exp_data_mean']
    exp_data_nn_w_be = all_value_dict['exp_data_nn']
    exp_data_max_w_be = all_value_dict['exp_data_max']

    # all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, 0)  # 0 means no BE flows
    #
    # exp_data_mean_wo_be = all_value_dict['exp_data_mean']
    # exp_data_nn_wo_be = all_value_dict['exp_data_nn']

    # f = plt.subplot(2, 1, 1)

    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()



    # Average
    flow_index = number_of_RT_flow_list.index(6)
    x, y = compute_ecdf(exp_data_mean_w_be[flow_index], "delay")
    ax1.plot(x, y, linestyle='--', alpha=alpha, color="b", marker="+", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='Mean Delay')

    # flow_index = number_of_RT_flow_list.index(6)
    # x, y = compute_ecdf(exp_data_mean_w_be[flow_index], "delay")
    # plt.plot(x, y, linestyle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='5 Flows')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('Mean Delay ($\mu$s)', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    plt.gca().set_xlim([0, common_xlim])

    plt.gca().legend(loc='lower right')

    fig.set_tight_layout(True)


    fig.set_tight_layout(True)

    # plt.subplot(2, 1, 2)

    # 99th percentile
    # flow_index = number_of_RT_flow_list.index(2)
    # x, y = compute_ecdf(exp_data_nn_w_be[flow_index], "delay")
    # plt.plot(x, y, linestyle='--', alpha=alpha, color="b", marker="+", markerfacecolor="None", markersize=8,
    #          markeredgewidth=1.5, linewidth=2, label='2 Flows')

    flow_index = number_of_RT_flow_list.index(6)
    x, y = compute_ecdf(exp_data_nn_w_be[flow_index], "delay")
    ax1.plot(x, y, linestyle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8,
             markeredgewidth=1.5, linewidth=2, label='99th Percentile Delay')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('99th Percentile Delay ($\mu$s)', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    plt.gca().set_xlim([0, common_xlim])

    plt.gca().legend(loc='lower right')

    flow_index = number_of_RT_flow_list.index(6)
    x, y = compute_ecdf(exp_data_max_w_be[flow_index], "delay")
    ax2.plot(x, y, linestyle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8,
             markeredgewidth=1.5, linewidth=2, label='Worst-case Delay')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('Worst-case Delay ($\mu$s)', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    plt.gca().set_xlim([0, common_xlim])

    plt.gca().legend(loc='lower right')

    fig.set_tight_layout(True)
    fig.savefig('delay_mean_99p.pdf', bbox_inches='tight')

    plt.show()



def get_delay_by_flow_number(data, flow_list, target_flow_number):

    flow_index = flow_list.index(target_flow_number)
    delay = data[flow_index]
    delay = [x for x in delay if x != -1]  # remove invalid entries

    return delay


def box_plot_try(filename, fignum=1):
    fig = plt.figure(fignum)
    common_ylim = 40

    plt.hold(True)

    alpha = 0.6

    number_of_RT_flow_list, number_of_BE_flow_list, number_of_test_cases, measurement_rates, delay_budget, output_data_list = get_back_objects(
        filename)

    n_BE_flows = number_of_BE_flow_list[0]  # index one means no BE flows

    all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, n_BE_flows)

    exp_data_mean_w_be = all_value_dict['exp_data_mean']
    exp_data_nn_w_be = all_value_dict['exp_data_nn']
    exp_data_max_w_be = all_value_dict['exp_data_max']

    delay_list = []
    # 99th percentile

    # we have 5 flows
    #for i in range(1, 5+1, 1):
    for i in range(0, len(number_of_RT_flow_list)):
        # delay = get_delay_by_flow_number(exp_data_nn_w_be, number_of_RT_flow_list, number_of_RT_flow_list[i])
        delay = get_delay_by_flow_number(exp_data_mean_w_be, number_of_RT_flow_list, number_of_RT_flow_list[i])
        # delay = get_delay_by_flow_number(exp_data_max_w_be, number_of_RT_flow_list, number_of_RT_flow_list[i])
        delay_list.append(delay)


    print delay_list


    plt.subplot(2, 1, 1)

    # plt.boxplot(delay_list, 1)
    boxprops = dict(linestyle='-', linewidth=1.1)
    plt.boxplot(delay_list, 0, 'g', boxprops=boxprops)
    # plt.boxplot(delay_list, 1, '')
    # plt.show()

    # labels = [2, 3, 4, 5, 6, 7]
    plt.ylabel('Delay ($\mu$s)', fontsize=15)
    plt.xlabel('Number of Flows', fontsize=15)
    plt.tick_params(axis='both', labelsize=12)
    plt.xticks([1, 2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 7])

    plt.gca().set_ylim([0, common_ylim])

    fig.set_tight_layout(True)
    fig.savefig('boxplot_99p.pdf', bbox_inches='tight')

    plt.show()



def plot_mean_delay_rtss_with_be_flows(filename, fignum=1):

    fig = plt.figure(fignum)
    common_xlim = 40
    plt.subplot(2, 1, 1)

    plt.hold(True)

    alpha = 0.9

    number_of_RT_flow_list, number_of_BE_flow_list, number_of_test_cases, measurement_rates, delay_budget, output_data_list = get_back_objects(
        filename)

    n_BE_flows = number_of_BE_flow_list[0]  # index one means no BE flows


    all_value_dict = extract_data_for_all_flow_list(number_of_RT_flow_list, output_data_list, n_BE_flows)

    exp_data_mean_w_be = all_value_dict['exp_data_mean']
    exp_data_nn_w_be = all_value_dict['exp_data_nn']
    exp_data_max_w_be = all_value_dict['exp_data_max']



    # Average
    flow_index = number_of_RT_flow_list.index(6)
    x, y = compute_ecdf(exp_data_mean_w_be[flow_index], "delay")
    plt.plot(x, y, linestyle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2,
             #label='Mean Delay'
             )

    # flow_index = number_of_RT_flow_list.index(6)
    # x, y = compute_ecdf(exp_data_mean_w_be[flow_index], "delay")
    # plt.plot(x, y, linestyle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='5 Flows')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('Delay ($\mu$s)', fontsize=15)
    # plt.tick_params(axis='both', labelsize=12)
    plt.gca().set_xlim([0, common_xlim])

    #plt.gca().legend(loc='lower right')

    fig.set_tight_layout(True)
    fig.savefig('delay_rtss.pdf', bbox_inches='tight')

    plt.show()



if __name__ == "__main__":
    # filename = 'timing_traces_rtss17.pickle'
    filename = 'timing_traces_rtss17_cam3.pickle'
    # plot_without_be_flows(filename, 1)


    # plot_mean_delay_with_be_flows(filename, 1)
    # plot_99p_delay_with_be_flows(filename, 2)
    # plot_max_delay_with_be_flows(filename, 3)

    # box_plot_try(filename, 1)

    # plot_mean_and_99p_and_max_delay_with_be_flows(filename, 1)

    # for RTSS17
    # plot_mean_and_99p_delay_with_be_flows(filename, 1)
    # plot_max_delay_with_be_flows(filename, 1)
    box_plot_try(filename, 1)
    # plot_mean_delay_rtss_with_be_flows(filename)
