import matplotlib.pyplot as plt
import xlrd
import numpy as np
import json
import os.path

d = {"d_diff": [], "d_same": []}

if os.path.exists("4flows_with_background/raw_data.json"):
    with open('4flows_with_background/raw_data.json', 'r') as fp:
        d = json.load(fp)
else:
    loc = ("4flows_with_background/summary_bg_diff_paths.xlsx")
    wb = xlrd.open_workbook(loc)
    for sheet_num in [1, 2, 3, 4]:
        sheet = wb.sheet_by_index(sheet_num)
        for i in range(2, sheet.nrows):
            d["d_diff"].append(sheet.cell_value(i, 3))

    loc = ("4flows_with_background/summary_bg_same_paths.xlsx")
    wb = xlrd.open_workbook(loc)
    for sheet_num in [1, 2, 3, 4]:
        sheet = wb.sheet_by_index(sheet_num)
        for i in range(2, sheet.nrows):
            d["d_same"].append(sheet.cell_value(i, 3))

    with open('4flows_with_background/raw_data.json', 'w') as fp:
        json.dump(d, fp)


fig, ax = plt.subplots(1, 1, figsize=(8, 5), frameon=False)
ax.boxplot([np.log10(d["d_same"]), np.log10(d["d_diff"])])

ax.set_xlabel('Hops in the path of $f_{4}$', fontsize=40, labelpad=10)
ax.set_ylabel('$Log_{10}$ of the End-to-End Delay (us)', fontsize=40, labelpad=25)
ax.set_xticklabels(('3', '4'), fontsize=35)
ax.set_yticklabels(('5.0', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5'), fontsize=35)

plt.show()
