import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from data_summary import get_data_dict, periods_str, num_switches_strs, payloads_strs

data_dict = get_data_dict()

n_groups = 4
fig, ax = plt.subplots(1, 1, figsize=(8, 5), frameon=False)
index = np.arange(n_groups)
bar_width = 0.45

error_config = dict(ecolor='black', alpha=0.7, lw=5, capsize=5, capthick=7)

hatches = ['', '', '/', '/']
opacities = [0.7, 1.0, 0.7, 1.0]

i = 0

for period_str in periods_str:

    if period_str == '1000ms':
        continue

    for payload_str in payloads_strs:

        if payload_str == '512B' or payload_str == '1024B':
            continue

        means = []
        stdevs = []

        for num_switches_str in num_switches_strs:
            mean = data_dict[period_str][num_switches_str][payload_str]["mean"]
            stdev = data_dict[period_str][num_switches_str][payload_str]["stdev"]
            sterr = stats.sem(data_dict[period_str][num_switches_str][payload_str]['raw'])
            means.append(mean)
            stdevs.append(stdev)

        label_str = "Period:" + period_str + ", Payload:" + payload_str

        rects = ax.bar(index + i * bar_width,
                       means,
                       bar_width,
                       alpha=opacities[i],
                       color='grey',
                       hatch=hatches[i],
                       yerr=sterr * 2.576 * 2,
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
ax.set_ylabel('End-to-End Delay (us)', fontsize=40, labelpad=25)
ax.set_xticks(index + bar_width * 4 / 4)
ax.set_xticklabels(('1', '2', '3', '4'), fontsize=35)
ax.set_yticklabels(('0', '100', '200', '300', '400', '500', '600'), fontsize=35)

ax.legend(ncol=2,
          fontsize=35,
          loc='upper center',
          bbox_to_anchor=[0.5, -0.4],
          shadow=True,
          fancybox=True)


fig.tight_layout()
plt.subplots_adjust(left=0.15, right=0.85, top=0.95, bottom=0.45)
plt.show()
