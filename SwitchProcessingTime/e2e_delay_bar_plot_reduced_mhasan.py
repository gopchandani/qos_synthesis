import numpy as np
import matplotlib.pyplot as plt
# matplotlib.use('TkAgg')
from scipy import stats
import re
from data_summary import get_data_dict, periods_str, num_switches_strs, payloads_strs

data_dict = get_data_dict()

def digit_text_seperator(digittext):

	match = re.match(r"([0-9]+)([a-z]+)", digittext, re.I)
	if match:
		items = match.groups()

	digit = items[0]
	text = items[1]
	
	return digit, text

# change font to Arial
plt.rcParams["font.family"] = "Arial"
plt.rcParams['font.size'] = 15
plt.rcParams['legend.fontsize'] = 13
plt.rcParams['axes.titlesize'] = 15
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 10

outfilename = 'end-to-end-delays-reduced-fixed.pdf'

tick_labelsize = 16
font_size = 19
legend_fontsize = 16

n_groups = 4

# fig, ax = plt.subplots(1, 1, figsize=(10, 5), frameon=True)
fig, ax = plt.subplots(1, 1)

index = np.arange(n_groups)
bar_width = 0.20

error_config = dict(ecolor='black', alpha=0.7, lw=5, capsize=5, capthick=7)

hatches = ['', '', '/', '+']
opacities = [0.7, 1.0, 0.7, 1.0]

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
            sterr = stats.sem(data_dict[period_str][num_switches_str][payload_str]['raw'])
            means.append(mean)
            stdevs.append(stdev)


        print means
        print stdevs
        d1, t1 = digit_text_seperator(period_str)
        d2, t2 = digit_text_seperator(payload_str)
        period_text = d1 + ' ' + t1
        payload_text = d2 + ' Bytes'
        
        label_str = "Period: " + period_text + ", Payload: " + payload_text

        rects = ax.bar(index + i * bar_width,
                       means,
                       bar_width,
                       alpha=opacities[i],
                       color='grey',
                       edgecolor='k',
                       hatch=hatches[i],
                       yerr=sterr * 2.576 * 2,
                       error_kw=error_config,
                       label=label_str)

        i += 1




# Hide the right and top spines
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)

# Adjust spacing between labels and axes
ax.tick_params(axis='x', which='major', pad=15)
ax.tick_params(axis='y', which='major', pad=15)

# ax.set_xlabel('Number of Switches', fontsize=40, labelpad=25)
# ax.set_ylabel('End-to-End Delay (us)', fontsize=40, labelpad=25)
# ax.set_xticks(index + bar_width * 4 / 2)
# ax.set_xticklabels(('1', '2', '3', '4'), fontsize=35)
# ax.set_yticklabels(('100', '200', '300', '400', '500', '600', '700'), fontsize=35)

# ax.set_ylim([100, 1000])

ax.set_xlabel('Number of Switches', fontsize=font_size)
ax.set_ylabel('End-to-End Delay ($\mu$s)', fontsize=font_size)
ax.set_xticks(index + bar_width * 4 / 2 - bar_width/2)
ax.set_xticklabels(('1', '2', '3', '4'), fontsize=tick_labelsize)
ax.set_yticklabels(('100', '200', '300', '400', '500', '600', '700'), fontsize=tick_labelsize)

ax.legend(ncol=2,
          fontsize=legend_fontsize,
          loc='upper center',
          bbox_to_anchor=[0.5, -0.4],
          shadow=False,
          fancybox=False)

# fig.tight_layout()
plt.subplots_adjust(left=0.1, right=0.99, top=0.80, bottom=0.45)


plt.savefig(outfilename, pad_inches=0.1, bbox_inches='tight')

plt.show()
