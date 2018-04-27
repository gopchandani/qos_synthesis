import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

from data_summary import get_data_dict, periods_str, num_switches_strs, payloads_strs

data_dict = get_data_dict()

n_groups = 4
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.2

opacity = 0.4
error_config = {'ecolor': '0.3'}

colors = ['black', 'red', 'green', 'blue']
i = 0

for period_str in periods_str:

    for payload_str in payloads_strs:

        if payload_str == '512B' or payload_str == '1024B':
            continue

        means = []
        stdevs = []

        for num_switches_str in num_switches_strs:
            mean = np.mean(data_dict[period_str][num_switches_str][payload_str])
            stdev = np.std(data_dict[period_str][num_switches_str][payload_str])

            means.append(mean)
            stdevs.append(stdev)

        print means
        print stdevs

        rects = ax.bar(index + i * bar_width, means, bar_width,
                        alpha=opacity, color=colors[i],
                        yerr=stdevs, error_kw=error_config,
                        label='Laptops,  Period: 100ms, Payload: 256B')
        i += 1


ax.set_xlabel('Number of Switches', fontsize=16)
ax.set_ylabel('End-to-End Delay (ns)', fontsize=16)
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(('1', '2', '3', '4'), fontsize=14)
ax.legend(loc=0, ncol=2, fontsize=10)

fig.tight_layout()
plt.show()

exit(0)
#
# n_groups = 4
#
# means_1 = (20, 35, 30, 35)
# std_1 = (2, 3, 4, 1)
#
# means_2 = (25, 32, 34, 25)
# std_2 = (3, 5, 2, 3)
#
# means_3 = (20, 35, 30, 35)
# std_3 = (2, 3, 4, 1)
#
# means_4 = (25, 32, 34, 25)
# std_4 = (3, 5, 2, 3)
#
# fig, ax = plt.subplots()
#
# index = np.arange(n_groups)
# bar_width = 0.2
#
# opacity = 0.4
# error_config = {'ecolor': '0.3'}
#
# rects1 = ax.bar(index, means_1, bar_width,
#                 alpha=opacity, color='black',
#                 yerr=std_1, error_kw=error_config,
#                 label='Laptops,  Period: 100ms, Payload: 256B')
#
# rects2 = ax.bar(index + 1 * bar_width, means_2, bar_width,
#                 alpha=opacity, color='r',
#                 yerr=std_2, error_kw=error_config,
#                 label='Laptops,  Period: 100ms, Payload: 1408B')
#
# rects3 = ax.bar(index + 2 * bar_width, means_3, bar_width,
#                 alpha=opacity, color='g',
#                 yerr=std_3, error_kw=error_config,
#                 label='Raspberry Pis,  Period: 1000ms, Payload: 256B')
#
# rects4 = ax.bar(index + 3 * bar_width, means_4, bar_width,
#                 alpha=opacity, color='blue',
#                 yerr=std_4, error_kw=error_config,
#                 label='Raspberry Pis,  Period: 1000ms, Payload: 1408B')
#
# ax.set_xlabel('Number of Switches', fontsize=16)
# ax.set_ylabel('End-to-End Delay (ns)', fontsize=16)
# ax.set_xticks(index + bar_width / 2)
# ax.set_xticklabels(('1', '2', '3', '4'), fontsize=14)
# ax.legend(loc=0, ncol=2, fontsize=10)
#
# fig.tight_layout()
# plt.show()
