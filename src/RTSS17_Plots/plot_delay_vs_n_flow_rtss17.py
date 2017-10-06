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


def plot_mean_delay_rtss_with_be_flows(filename, fignum=1):

    fig = plt.figure(fignum)
    common_xlim = 80
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
    flow_index = number_of_RT_flow_list.index(3)
    x, y = compute_ecdf(exp_data_mean_w_be[flow_index], "delay")
    plt.plot(x, y, linestyle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2,
             #label='Mean Delay'
             )

    # flow_index = number_of_RT_flow_list.index(6)
    # x, y = compute_ecdf(exp_data_mean_w_be[flow_index], "delay")
    # plt.plot(x, y, linestykkle='-', alpha=alpha, color="k", marker=".", markerfacecolor="None", markersize=8, markeredgewidth=1.5, linewidth=2, label='5 Flows')

    plt.ylabel('Empirical CDF', fontsize=15)
    plt.xlabel('Delay ($\mu$s)', fontsize=15)
    # plt.tick_params(axis='both', labelsize=12)
    plt.gca().set_xlim([0, common_xlim])

    #plt.gca().legend(loc='lower right')

    fig.set_tight_layout(True)
    fig.savefig('delay_rtss.pdf', bbox_inches='tight')

    plt.show()



if __name__ == "__main__":

    filename = 'objs.pickle.sp.2.40.10iter'
    #filename = 'objs.pickle.mcp.2.4'
    #filename = 'objs.pickle.simple.mcp'
    filename = 'objs.pickle'


    plot_mean_delay_rtss_with_be_flows(filename)

