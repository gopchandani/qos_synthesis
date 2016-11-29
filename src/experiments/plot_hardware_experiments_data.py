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
        mean = np.mean(data_dict[p])
        sem = ss.sem(data_dict[p])
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

    prefix = "hardware_experiments_data/"

    with open(prefix + "h1s1_to_h1s2.json", "r") as in_file:
        h1s1_to_h1s2 = json.loads(in_file.read())

    with open(prefix + "h2s1_to_h2s2.json", "r") as in_file:
        h2s1_to_h2s2 = json.loads(in_file.read())

    reshuffled_data = dict()
    reshuffled_data["h1s1_to_h1s2"] = prepare_reshuffled_data(h1s1_to_h1s2, "mean_latency")
    reshuffled_data["h2s1_to_h2s2"] = prepare_reshuffled_data(h2s1_to_h2s2, "mean_latency")

    aa = plot_lines_with_error_bars()


if __name__ == "__main__":
    main()


