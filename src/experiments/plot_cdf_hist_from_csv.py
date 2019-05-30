import os, csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.text as t
import scipy.stats as stats
import subprocess


location_of_data = "/home/ak7/Desktop/RTSS/RTSS_May24" # Give the directory here ending in the experiment name
location_of_rawdata = "/home/ak7/Desktop/RTSS/RTSS_May24/raw_data"
experiment = location_of_rawdata.split('/')[5]
path_roots = list()
# type_of_experiment = "bg" # bg or noback
# type_of_experiment = "noback"

# Non-overlapping background & RT Flows
# path_roots = [os.path.join(location_of_data,"f5")]
# title = "Non-overlapping background & RT Flows"

# Background & RT Flows share a node
# path_roots = [os.path.join(location_of_data,"f1"),
#               os.path.join(location_of_data,"f2"),
#               os.path.join(location_of_data,"f7")]
# title = "Background & RT Flows share a node"

# Background & RT Flows along same path
path_roots = [ #os.path.join(location_of_data,"f4"),
              os.path.join(location_of_data,"f8")]
title = "Background & RT Flows along same path"

color_list = ['g', 'b']

## Plotting settings
plt.rcdefaults()
plt.rcParams["font.family"] = "Arial"
plt.rcParams['font.size'] = 20
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['figure.figsize'] = 8, 6

# Plot all the csv's in the directory path_root individually
def plot_csv_simple(path_root):
    for filename in os.listdir(os.path.abspath(path_root)):
        print("Filename %s\n"%(filename))
        if filename.endswith(".csv"):
            plt.clf()
            # print("*******", filename)
            title = "CDF" + "_" + ((filename.split('.'))[0].split('_'))[0] + "-" + type_of_experiment
            app_diff = list()

            with open(os.path.join(path_root, filename), 'r', newline='') as csvfile:
                # next(csvfile)
                readCSV = csv.reader(csvfile, delimiter=' ')
                for row in readCSV:
                    # print(row[3])
                    # print(row[1])
                    if row[1] is not None:
                        # print(row[1])
                        try:
                            # app_diff_val = int(row[3]) / 1000
                            app_diff_val = float(row[1])

                            app_diff.append(app_diff_val)
                            # if app_diff > 10:
                            #     app_diffs_clipped.append(0)
                            # else:
                            #     app_diffs_clipped.append(app_diff)
                            #
                        except ValueError:
                            pass
                            # print(int(row[1]))

            app_diff_1=reject_outliers(np.array(app_diff))

            x = np.sort(app_diff_1)
            y = np.arange(1, len(x) + 1) / len(x)

            plt.ylim(0.0, 1.0)
            plt.xlim(0.0,1000.0)
            fig = plt.plot(x, y, label=str(filename), marker='.', linestyle='none')
            # leg_loc = plt.legend(loc='upper left')
            plt.xlabel('End to End delays (' + u'\u03BC' + 's)')
            plt.ylabel('CDF')
            plt.margins(0.02)
            plt.title(title + experiment)
            name_of_fig = '.'.join([title + '-' + (path_root.split('_'))[14], "png"])
            plt.savefig(os.path.join(path_root, name_of_fig))

def plot_99point9th_percentile(path_root, type_of_experiment, flow_id, title):
    # run_nums = []
    # run_num = 1

    csv_run_nums=[]
    csv_run_num = 1

    ninety_nineth_percentile_vals = list()
    ninety_nine_point_three_percentile_vals = list()
    ninety_nine_point_five_percentile_vals = list()
    ninety_nine_point_nine_percentile_vals = list()

    averages = list()
    min_vals=list()
    max_vals=list()
    median_vals=list()
    num_above = 0
    # big_array=list()
    # two_np_array=np.empty([2,100001])

    for root_dir, sub_dirs, files in os.walk(os.path.join(path_root, type_of_experiment)):
        # print(root_dir, sub_dirs, files)

        sub_dirs.sort()
        if files:
            # i=1
            for filename in files:

                if filename.endswith(".csv") and filename.find(flow_id) >= 0:# and int(root_dir.split('_')[-3]) in [1,2]:

                    # plt.clf()
                    print("*******", os.path.join(root_dir,filename))
                    title = " Flow Latency Statistics" + ":" + " RT Traffic only"
                    # title = " Flow Latency Statistics" + ":" + " RT with Background Traffic"
                    app_diff = list()

                    with open(os.path.join(root_dir, filename), 'r', newline='') as csvfile:
                        # next(csvfile)
                        readCSV = csv.reader(csvfile, delimiter=' ')
                        for row in readCSV:
                            # print(row[3])
                            # print(row[1])
                            if row[1] is not None:
                                # print(row[1])
                                try:
                                    # app_diff_val = int(row[3]) / 1000
                                    app_diff_val = float(row[1])

                                    app_diff.append(app_diff_val)
                                    # if app_diff > 10:
                                    #     app_diffs_clipped.append(0)
                                    # else:
                                    #     app_diffs_clipped.append(app_diff)
                                    #
                                except ValueError:
                                    pass
                                    # print(int(row[1]))

                    min_val = np.min(app_diff)
                    min_vals.append(min_val)

                    max_val = np.max(app_diff)
                    max_vals.append(max_val)

                    median_val = np.percentile(app_diff,50.0)
                    median_vals.append(median_val)

                    ninety_nineth_percentile_val = np.percentile(app_diff, 99.0)
                    ninety_nineth_percentile_vals.append(ninety_nineth_percentile_val)

                    ninety_nine_point_three_percentile_val = np.percentile(app_diff, 99.3)
                    ninety_nine_point_three_percentile_vals.append(ninety_nine_point_three_percentile_val)

                    ninety_nine_point_five_percentile_val = np.percentile(app_diff, 99.5)
                    ninety_nine_point_five_percentile_vals.append(ninety_nine_point_five_percentile_val)

                    ninety_nine_point_nine_percentile_val = np.percentile(app_diff, 99.9)
                    ninety_nine_point_nine_percentile_vals.append(ninety_nine_point_nine_percentile_val)

                    avg = np.mean(app_diff)
                    averages.append(avg)

                    csv_run_num = (root_dir.split('_'))[-3]
                    csv_run_nums.append(int(csv_run_num))

                    app_diff_as_numpy = np.asarray(app_diff)
                    var = app_diff_as_numpy[app_diff_as_numpy > 550]
                    num_above += len(var)

                    # plt.boxplot(app_diff_as_numpy)
                    # plt.ion()
                    # two_np_array [i, :] =  app_diff_as_numpy
                    # np.concatenate( app_diff)




                    # i = i +1
    #print(ninetyninepointnine)
    plt.ylim([0.0,7000.0])
    plt.xticks([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    plt.yticks([500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000,6500, 7000])

    # print(two_np_array.shape)
    #
    # plt.boxplot(two_np_array)

    # plt.boxplot(csv_run_nums, min_vals)#, 'ob',  label='minimum')
    # plt.boxplot(csv_run_nums, averages)#, 'og', label='mean')
    # plt.boxplot(csv_run_nums,median_vals)#, 'or', label='median')
    # plt.boxplot(csv_run_nums, ninety_nineth_percentile_vals)#, 'oc', label='99.0 $\%^{ile}$')
    # plt.boxplot(csv_run_nums, ninety_nine_point_three_percentile_vals)#, 'om', label='99.3 $\%^{ile}$')
    # plt.boxplot(csv_run_nums, ninety_nine_point_five_percentile_vals)#, 'ok', label='99.5 $\%^{ile}$')
    # plt.boxplot(csv_run_nums, ninety_nine_point_nine_percentile_vals)#, 'oy', label='99.9 $\%^{ile}$')

    #plt.subplot(1,2,1)
    plt.plot(csv_run_nums, min_vals, 'bs', label='minimum')
    plt.plot(csv_run_nums, averages, 'go', label='mean')
    plt.plot(csv_run_nums, median_vals, 'y*', label='median')
    plt.plot(csv_run_nums, ninety_nineth_percentile_vals, 'cD', label='99.0p')
    plt.plot(csv_run_nums, ninety_nine_point_three_percentile_vals, 'mx', label='99.3p')
    plt.plot(csv_run_nums, ninety_nine_point_five_percentile_vals, 'kh', label='99.5p')
    plt.plot(csv_run_nums, ninety_nine_point_nine_percentile_vals, 'r+', label='99.9p')

    # plt.plot(csv_run_nums, min_vals, label='minimum')
    # plt.plot(csv_run_nums, averages, label='mean')
    # plt.plot(csv_run_nums,median_vals, label='median')
    # plt.plot(csv_run_nums, ninety_nineth_percentile_vals, label='99.0 percentile')
    # plt.plot(csv_run_nums, ninety_nine_point_three_percentile_vals, label='99.3 percentile')
    # plt.plot(csv_run_nums, ninety_nine_point_five_percentile_vals, label='99.5 percentile')
    # plt.plot(csv_run_nums, ninety_nine_point_nine_percentile_vals, label='99.9 percentile')

    plt.title(title)
    #plt.ylabel('End to End delays (' + u'\u03BC' + 's)')
    plt.ylabel('End to End Delay ($\mu$s)')
    plt.xlabel('Iteration # of Experiment')
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    plt.legend(loc='upper center', prop={'size': 14}, fancybox=False, shadow=False, ncol=4)
    #plt.legend(loc='upper center', prop={'size':10}, bbox_to_anchor=(0.5, -0.20), fancybox=True, shadow=True, ncol=4)
    plt.tight_layout()

    #plt.hist(diffs, label='99.9th', bins=5, alpha=0.5, color='g')
    plt.savefig(os.path.join(path_root, type_of_experiment, 'max-min-f8-scatter-nobg.pdf'), pad_inches=0.05, bbob_inches='tight')
    plt.show()
    print(num_above)


#path root is the location of the raw_data
def find_all_csvs_for_flow_and_plot_combined(path_root, type_of_experiment, flow_id, title):
    plt.clf()
    for root_dir, sub_dirs, files in os.walk(os.path.join(path_root, type_of_experiment)):
        if files:
            for filename in files:
                if filename.find(flow_id) != -1 and filename.endswith('csv'):
                    print("Analysing csv file : %s\n"%(os.path.join(root_dir, filename)))
                    # plot_csv_simple(os.path.abspath(root_dir, filename))
                    # plt.clf()
                    # print("*******", filename)
                    heading = "CDF" + "_" + (str((filename.split('.'))[0]).split('_'))[0] + \
                              " - " + type_of_experiment + title
                    app_diff = list()

                    with open(os.path.join(root_dir, filename), 'r', newline='') as csvfile:
                        # next(csvfile)
                        readCSV = csv.reader(csvfile, delimiter=' ')
                        for row in readCSV:
                            # print(row[1])
                            if row[1] is not None:
                                # print(row[1])
                                try:
                                    # app_diff_val = int(row[3]) / 1000
                                    app_diff_val = float(row[1])

                                    app_diff.append(app_diff_val)
                                    # if app_diff > 10:
                                    #     app_diffs_clipped.append(0)
                                    # else:
                                    #     app_diffs_clipped.append(app_diff)
                                    #
                                except ValueError:
                                    pass
                                    # print(int(row[1]))

                    app_diff_1=reject_outliers(np.array(app_diff),99.9)

                    x = np.sort(app_diff_1)
                    y = np.arange(1, len(x) + 1) / len(x)

                    plt.ylim(0.0, 1.0)
                    plt.xlim(0.0,1000.0)
                    fig = plt.plot(x, y, label=(root_dir.split('_'))[-1], marker='.', linestyle='none')
                    leg_loc = plt.legend(loc='upper right')
                    #fig = plt.plot(x, y, marker='.', linestyle='none')
                    plt.xlabel('End to End delays (' + u'\u03BC' + 's)')
                    plt.ylabel('CDF')
                    plt.margins(0.05)
                    plt.title(heading + experiment)
            name_of_combined_fig = 'individual_runs_' + flow_id + '-' + type_of_experiment
            plt.savefig(os.path.join(path_root, type_of_experiment, name_of_combined_fig))


# Top plot the comparative histogram, overlapping two histograms in a figure
def plot_hist_comparison(path_root):
    percentile = 100.0
    path_root = path_root + '/'
    c_i = 0
    plt.clf()
    for filename in os.listdir(path_root):
        c_i = c_i + 1
        if filename.endswith(".csv"):
            print("*******", filename)
            app_diff = list()
            with open(path_root + filename, 'r', newline='') as csvfile:
                next(csvfile)
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    # print(row[3])
                    if row[1] is not None:
                        try:
                            #app_diff_val = int(row[1])/1000
                            app_diff_val = float(row[1])
                            app_diff.append(app_diff_val)

                        except ValueError:
                            pass


            app_diff_1 = reject_outliers(np.array(app_diff), percentile)
            if filename.find('BG') >= 0:
                rtbg_owt = list(app_diff_1)
            else:
                rt_owt = list(app_diff_1)

    plt.axvline(x=900.0, color='r', lw=2)
    # plt.axvline(x=900.0, color='r', label='Deadline of Flow $F_8$', lw=2)
    _ = plt.hist(rtbg_owt, bins=200, label='RT with Background Traffic', alpha=0.5, color='#d95f02')
    _ = plt.hist(rt_owt,  bins=200, label='RT Traffic Only', alpha=0.5, color='#7570b3')
    # plt.ylim(0.0, 1000000.0)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.xlim(0.0,1000.0)
    plt.ylim(0.0, 5.5E6)
    # plt.axvline(900)


    plt.xlabel('End to End Delay ($\mu$s)')
    plt.ylabel('Packet Count')
    # plt.title('Priority/Queue-based Traffic Isolation')

    plt.legend(loc='upper left', prop={'size': 14}, fancybox=False, shadow=False, ncol=1)
    plt.text(850, 3.5E6, 'Deadline = 900.0 $\mu$s',  rotation=90)

    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=False, shadow=False, ncol=2)
    # plt.legend()
    # plt.legend(loc='lower left', bbox_to_anchor=(0.0, 1.01), ncol=3, borderaxespad=0, frameon=False )#bbox_to_anchor=(1.04, 1), fancybox=True, shadow=True)
    plt.savefig(os.path.join(path_root, 'hist-f8.pdf'), pad_inches=0.05, bbob_inches='tight')
    plt.tight_layout()
    plt.show()

# To plot comparative CDFs
# Please check CSV format
def plot_cdf_comparison(path_root):
    percentile=99.9
    path_root = path_root + '/'
    plt.clf()
    for filename in os.listdir(path_root):
        if  filename.endswith(".csv"):
            print("*******", filename)
            app_diff = list()
            app_diffs_clipped = []
            rowcount = 0
            with open(path_root + filename, 'r', newline='') as csvfile:
                next(csvfile)
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    # print(row[3])
                    # print(row[0])
                    if row[1] is not None:
                        # print(row[1])
                        try:
                            # app_diff_val = int(row[3]) / 1000
                            app_diff_val = float(row[1])
                            app_diff.append(app_diff_val)
                            # if app_diff > 10:
                            #     app_diffs_clipped.append(0)
                            # else:
                            #     app_diffs_clipped.append(app_diff)
                            #

                        except ValueError:
                            pass
                            #print(int(row[1]))


            #print(app_diff)
            app_diff_1 = reject_outliers(np.array(app_diff), percentile)
            if filename.find('BG') >= 0 :
                rtbg_owt = list(app_diff_1)
            else:
                rt_owt = list(app_diff_1)


            x = np.sort(app_diff_1)
            y = np.arange(1, len(x) + 1) / len(x)
            plt.ylim(0.0, 1.0)
            plt.xlim(200.0, 1000.0)
            plt.plot(x, y, label=str(filename), marker='.', linestyle='none')
            leg_loc = plt.legend(loc='upper left')
            plt.xlabel('End to End delays (' + u'\u03BC' + 's)')
            plt.ylabel('CDF')
            plt.margins(0.02)
            plt.title(title + experiment)



            # with open(path_root + 'stats.txt', 'a') as f2:
            #     f2.write("%s\n" % (filename.split('.')[0] + " : " + print_stats(app_diff)))

    a, b = stats.ks_2samp(rt_owt, rtbg_owt)
    offset = t.OffsetFrom(leg_loc, (1.5, 0.0))
    val1 = 'K-S statistic = ' + str(round(a,2))
    val2 = 'P-value = ' + str(b)
    val3 = 'mean (no_bg) = ' + str(round(np.mean(rt_owt),3))
    val4 = 'mean (bg) = ' + str(round(np.mean(rtbg_owt),3))

    print(val3)
    print(val4)

    plt.annotate(val1, xy=(0, 0), xytext=(40, -10), size=10, xycoords='figure fraction',
                 textcoords=offset, horizontalalignment='right',
                 verticalalignment='top'
                 )

    plt.annotate(val2, xy=(0, 0), xytext=(200, -10), size=10, xycoords='figure fraction',
                 textcoords=offset, horizontalalignment='right',
                 verticalalignment='top'
                 )
    plt.annotate(val3, xy=(0, 0), xytext=(40, -40), size=10, xycoords='figure fraction',
                 textcoords=offset, horizontalalignment='right',
                 verticalalignment='top'
                 )

    plt.annotate(val4, xy=(0, 0), xytext=(200, -40), size=10, xycoords='figure fraction',
                 textcoords=offset, horizontalalignment='right',
                 verticalalignment='top'
                 )

    #plt.show()
    #print(os.path.join(path_root, path_root.split('/')[-2] + '_cdf_comparison_' + str(percentile)))
    plt.savefig(os.path.join(path_root, 'orig_' + path_root.split('/')[-2] + '_cdf_comparison_' + str(percentile)), format='png')
    print(a)
    print(b)

def print_stats(diffs):

    val = [ "Mean:" + str(np.mean(diffs)), "Stdev:" + str(np.std(diffs)), "Median:" + str(np.percentile(diffs, 50)),
                          "99th Percentile:" + str(np.percentile(diffs, 99)),
                          "99.9th Percentile:" + str(np.percentile(diffs, 99.9)),
                          "99.99th Percentile:" + str(np.percentile(diffs, 99.99)) ]

    output = " ".join(val)
    #print(output)
    return output

def reject_outliers(data, percentile, m=6):
    # Statistical Witchcraft -- Use with CAUTION
    # return data[abs(data - np.mean(data)) < m * np.std(data)]
    return data[abs(data) <= np.percentile(data, percentile)]

if __name__ == '__main__':

    ## Cleanup old png's
    ## Weirdly woldcards don't work in subprocess.call
    ## Subprocess.popen doesn't work with spaces in the filename -- need to escape it -- haven't figure that out
    # for root_dir, sub_dirs, files in os.walk(os.path.join(location_of_data, type_of_experiment)):
    #     for file in files:
    #         if file.endswith('.png'):
    #             #print("Root Dir %s File %s\n"%(root_dir, file))
    #             #subprocess.Popen("rm " + os.path.join(root_dir, sub_dir, "*.png"), shell=True)
    #             subprocess.Popen("rm " + os.path.join(root_dir, file), shell=True)


    # To recursively traverse a directory - use it if you want to go into each of the experiments
    # type_of_experiment defines the type of experiment such as bg, noback and so on
    #
    # for root_dir, sub_dirs, files in os.walk(os.path.join(location_of_data, type_of_experiment)):
    #     for sub_dir in sub_dirs:
    #         path_roots.append(os.path.join(location_of_data, type_of_experiment, sub_dir))

    # print(len(path_roots))

    # title = "Non-overlapping background & RT Flows"
    # # plot_99point9th_percentile(location_of_rawdata, type_of_experiment, 'f5', title)
    # plot_99point9th_percentile(location_of_rawdata, type_of_experiment, 'f4', title)
    # plot_99point9th_percentile(location_of_rawdata, type_of_experiment, 'f8', title)


    # List all directory
    for path_root in path_roots:
        print("Entering %s\n" %(path_root))
        # plot_csv_simple(path_root)
        plot_hist_comparison(path_root)
        plot_cdf_comparison(path_root)

    # title = "Background & RT Flows along same path"
    # find_all_csvs_for_flow_and_plot_combined(location_of_rawdata, type_of_experiment, 'f4', title)
    # find_all_csvs_for_flow_and_plot_combined(location_of_rawdata, type_of_experiment, 'f8', title)
    #
    # title = "Non-overlapping background & RT Flows"
    # find_all_csvs_for_flow_and_plot_combined(location_of_rawdata, type_of_experiment, 'f5', title)

