import json
import time
import random
import math
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pprint import pprint
from timer import Timer
from collections import defaultdict


def prepare_matplotlib_data(data_dict):

    x = sorted(data_dict.keys(), key=int)

    data_means = []
    data_sems = []

    for p in x:
        mean = np.mean(map(float, data_dict[p]))
        sem = ss.sem(map(float, data_dict[p]))
        data_means.append(mean)
        data_sems.append(sem)

    return x, data_means, data_sems


def plot_lines_with_error_bars(data,
                               ax,
                               data_key,
                               x_label,
                               y_label,
                               subplot_title,
                               y_scale,
                               x_min_factor=1.0,
                               x_max_factor=1.05,
                               y_min_factor=0.1,
                               y_max_factor=1.5,
                               xticks=None,
                               xtick_labels=None,
                               yticks=None,
                               ytick_labels=None):

    ax.set_xlabel(x_label, fontsize=10, labelpad=-0)
    ax.set_ylabel(y_label, fontsize=10, labelpad=0)
    ax.set_title(subplot_title, fontsize=10)

    markers = ['.', 'v', 'o', 'd', '+', '^', 'H', ',', 's', 'o', 'h', '*']
    marker_i = 0

    for line_data_key in data[data_key]:

        data_vals = data[data_key][line_data_key]

        x, mean, sem = prepare_matplotlib_data(data_vals)

        ax.errorbar(x, mean, sem, color="black", marker=markers[marker_i], markersize=6.0, label=line_data_key, ls='none')

        marker_i += 1

    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)

    low_xlim, high_xlim = ax.get_xlim()
    ax.set_xlim(xmax=(high_xlim) * x_max_factor)
    ax.set_xlim(xmin=(low_xlim) * x_min_factor)

    if y_scale == "linear":
        low_ylim, high_ylim = ax.get_ylim()
        ax.set_ylim(ymin=low_ylim*y_min_factor)
        ax.set_ylim(ymax=high_ylim*y_max_factor)
    elif y_scale == "log":
        ax.set_ylim(ymin=1)
        ax.set_ylim(ymax=100000)

    ax.set_yscale(y_scale)

    xa = ax.get_xaxis()
    xa.set_major_locator(MaxNLocator(integer=True))

    if xticks:
        ax.set_xticks(xticks)

    if xtick_labels:
        ax.set_xticklabels(xtick_labels)

    if yticks:
        ax.set_yticks(yticks)

    if ytick_labels:
        ax.set_yticklabels(ytick_labels)


def prepare_reshuffled_data(data, key_of_interest):
    reshuffled_data = defaultdict(list)

    for rate in data:
        for rate_dict in data[rate]:
            reshuffled_data[rate].append(rate_dict[key_of_interest])

    return reshuffled_data


def main():

    data_path_prefix = "hardware_experiments_data/"
    plots_path_prefix = "hardware_experiments_plots/"
    experiment_tag = "hardware_experiments"

    with open(data_path_prefix + "h1s1_to_h1s2_meters.json", "r") as in_file:
        h1s1_to_h1s2_meters = json.loads(in_file.read())

    with open(data_path_prefix + "h2s1_to_h2s2_meters.json", "r") as in_file:
        h2s1_to_h2s2_meters = json.loads(in_file.read())

    with open(data_path_prefix + "h1s1_to_h1s2_no_meters.json", "r") as in_file:
        h1s1_to_h1s2_no_meters = json.loads(in_file.read())

    with open(data_path_prefix + "h2s1_to_h2s2_no_meters.json", "r") as in_file:
        h2s1_to_h2s2_no_meters = json.loads(in_file.read())

    data = {
        "Mean Latency": defaultdict(defaultdict),
        "99th Percentile Latency": defaultdict(defaultdict),
    }

    data["Mean Latency"]["h1s1 -> h1s2, Different Meter"] = prepare_reshuffled_data(h1s1_to_h1s2_meters, "mean_latency")

    data["Mean Latency"]["h2s1 -> h2s2, Different Meter"] = prepare_reshuffled_data(h2s1_to_h2s2_meters, "mean_latency")

    data["99th Percentile Latency"]["h1s1 -> h1s2, Different Meter"] = prepare_reshuffled_data(h1s1_to_h1s2_meters,
                                                                                               "nn_perc_latency")

    data["99th Percentile Latency"]["h2s1 -> h2s2, Different Meter"] = prepare_reshuffled_data(h2s1_to_h2s2_meters,
                                                                                               "nn_perc_latency")

    data["Mean Latency"]["h1s1 -> h1s2, No Meter"] = prepare_reshuffled_data(h1s1_to_h1s2_no_meters, "mean_latency")

    data["Mean Latency"]["h2s1 -> h2s2, No Meter"] = prepare_reshuffled_data(h2s1_to_h2s2_no_meters, "mean_latency")

    data["99th Percentile Latency"]["h1s1 -> h1s2, No Meter"] = prepare_reshuffled_data(h1s1_to_h1s2_no_meters,
                                                                                               "nn_perc_latency")

    data["99th Percentile Latency"]["h2s1 -> h2s2, No Meter"] = prepare_reshuffled_data(h2s1_to_h2s2_no_meters,
                                                                                               "nn_perc_latency")

    f, (ax2, ax3) = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(6.0, 3.0))
    f.tight_layout()

    data_xtick_labels = sorted(data["Mean Latency"]["h1s1 -> h1s2, Different Meter"].keys(), key=int)
    data_xticks = [int(x) for x in data_xtick_labels]

    plot_lines_with_error_bars(data,
                               ax2,
                               "Mean Latency",
                               "Flow Rate (Mbps)",
                               "Mean Latency (us)",
                               "",
                               y_scale='linear',
                               x_min_factor=0.98,
                               x_max_factor=1.02,
                               y_min_factor=0.9,
                               y_max_factor=1.05,
                               xticks=data_xticks,
                               xtick_labels=data_xtick_labels)

    plot_lines_with_error_bars(data,
                               ax3,
                               "99th Percentile Latency",
                               "Flow Rate (Mbps)",
                               "99th Percentile Latency (us)",
                               "",
                               y_scale='linear',
                               x_min_factor=0.98,
                               x_max_factor=1.02,
                               y_min_factor=0.9,
                               y_max_factor=1.05,
                               xticks=data_xticks,
                               xtick_labels=data_xtick_labels)

    xlabels = ax2.get_xticklabels()
    plt.setp(xlabels, rotation=0, fontsize=10)

    xlabels = ax3.get_xticklabels()
    plt.setp(xlabels, rotation=0, fontsize=10)

    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0 + box.height * 0.3, box.width, box.height * 0.7])

    box = ax3.get_position()
    ax3.set_position([box.x0, box.y0 + box.height * 0.3, box.width, box.height * 0.7])

    handles, labels = ax3.get_legend_handles_labels()

    ax2.legend(handles,
               labels,
               shadow=True,
               fontsize=10,
               loc='upper center',
               ncol=2,
               markerscale=1.0,
               frameon=True,
               fancybox=True,
               columnspacing=0.7, bbox_to_anchor=[1.1, -0.25])

    plt.savefig(plots_path_prefix + experiment_tag + "_" + "qos_demo" + ".png", dpi=200)
    plt.show()

if __name__ == "__main__":
    main()


