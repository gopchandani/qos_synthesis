import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

from data_summary import get_data_dict, periods_str, num_switches_strs, payloads_strs

data_dict = get_data_dict()

n_groups = 4
fig, ax = plt.subplots(1, 1, figsize=(10, 5), frameon=False)
index = np.arange(n_groups)
bar_width = 0.20

error_config = dict(ecolor='black', alpha=0.7, lw=5, capsize=5, capthick=7)

hatches = ['', '', '/', '/']
opacities = [1.0, 0.7, 1.0, 0.7]

i = 0

for period_str in periods_str:

    for payload_str in payloads_strs:

        if payload_str == '512B' or payload_str == '1024B':
            continue

        means = []
        stdevs = []

        for num_switches_str in num_switches_strs:
            mean = data_dict[period_str][num_switches_str][payload_str]["mean"]
            stdev = data_dict[period_str][num_switches_str][payload_str]["stdev"]
            means.append(mean)
            stdevs.append(stdev)


        print means
        print stdevs
        label_str = "Period:" + period_str + ", Payload:" + payload_str

        rects = ax.bar(index + i * bar_width,
                       means,
                       bar_width,
                       alpha=opacities[i],
                       color='grey',
                       hatch=hatches[i],
                       yerr=stdevs,
                       error_kw=error_config,
                       label=label_str)

        i += 1


# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Adjust spacing between labels and axes
ax.tick_params(axis='x', which='major', pad=15)
ax.tick_params(axis='y', which='major', pad=15)

ax.set_xlabel('Number of Switches', fontsize=40, labelpad=25)
ax.set_ylabel('End-to-End Delay (ns)', fontsize=40, labelpad=25)
ax.set_xticks(index + bar_width * 4 / 2)
ax.set_xticklabels(('1', '2', '3', '4'), fontsize=35)
ax.set_yticklabels(('100', '200', '300', '400', '500', '600', '700'), fontsize=35)

ax.legend(ncol=2,
          fontsize=30,
          loc='upper center',
          bbox_to_anchor=[0.5, -0.4],
          shadow=True,
          fancybox=True)

fig.tight_layout()
plt.subplots_adjust(left=0.1, right=0.99, top=0.95, bottom=0.38)
plt.show()
