# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"


#import matplotlib.pyplot as plt
import xlrd
import numpy as np
import json
import os.path



import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt




plt.show()

def get_data():
        
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
        print ("loc is", loc)
        wb = xlrd.open_workbook(loc)
        for sheet_num in [1, 2, 3, 4]:
            sheet = wb.sheet_by_index(sheet_num)
            for i in range(2, sheet.nrows):
                d["d_same"].append(sheet.cell_value(i, 3))
#    
        with open('4flows_with_background/raw_data.json', 'w') as fp:
            json.dump(d, fp)
    
    return d


if __name__ == '__main__':
    
    
     # change font to Arial
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams['font.size'] = 15
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['axes.titlesize'] = 15
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 10
    
    
    d = get_data()
    
    
    
    plt.subplot(2, 1, 1)
    ax = plt.gca() # grab the current axis
    
    flierprops = dict(marker='.', markersize=1,
                  linestyle='none', markerfacecolor='firebrick')
    
    ax.boxplot([np.log10(d["d_same"]), np.log10(d["d_diff"])],
                flierprops=flierprops)
    
    ax.set_xlabel('Number of Hops in the Path of Flow 4')
    ax.set_ylabel('End-to-End Delay ($\mu$s)\n  $log_{10}$ scale')
    ax.set_xticklabels(('3', '4'))
#    ax.set_yticklabels(('5.0', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5'))
    ax.set_ylim([5, 10])
    
    plt.savefig("motivating_results.pdf", pad_inches=0.1, bbox_inches='tight')
    plt.show()

    print("Script Finished!!")