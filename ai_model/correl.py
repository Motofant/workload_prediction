import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import pingouin as pg
from constants_correl import MODE, calc_weighted_target, calc_mean_target

# constants
to_convert = ["key_press_time","key_dead_time_avg"]
rename = {0:"keine",1:"0-Back", 2:"1-Back"}
single_target_col = "_mental"
target_col = "goal"
train_data = pd.DataFrame()
test_data = pd.DataFrame()
workload_mean = pd.DataFrame()
OUTPUT_PATH = "./correl_out/"
# variables
## target type
weighted = False
workload_level=True

## mode 
mode = MODE.PHRASE   

## statistics
correl = False
anova = True

# import path 
## Folder has to contain processed data + general_info.csv
FILE_PATH = "./processed_2_1apart/"
#FILE_PATH = "./processed_30_5apart/"


# read files
files = [f for f in os.listdir(FILE_PATH)]
general_info_data = pd.read_csv(FILE_PATH + "general_info.csv")
sorted_files = {}
label = {}

# sort to allow labeling
for f in files:
    split_str = f.split("_") 
    if "demand" in split_str[1]:
        label[split_str[0]] = f  
    elif split_str[0] not in sorted_files.keys():
        if any(task in f for task in mode.value):
            sorted_files[split_str[0]] = [f]
    else:
        if any(task in f for task in mode.value):
            sorted_files[split_str[0]].append(f)

train_data_lst = []
# labeling
for key,lst in sorted_files.items():
    print(FILE_PATH+label[key])

    # read demand file
    target = pd.read_csv(FILE_PATH+label[key]).to_dict(orient="records")[0]
    
    # add targetcolumn to data
    for i in lst:
        # read metrics into df
        read_data = pd.read_csv(FILE_PATH+i).fillna(0)
        read_data = read_data.replace("NaN",0)

        # convert times to 
        for val in to_convert:
            read_data[val] = pd.to_timedelta(read_data[val])/pd.Timedelta(seconds=1)

        # get target column
        if weighted:
            read_data[target_col] = calc_weighted_target(data_file = i, target = target)         

        if workload_level:
            read_data[target_col] = general_info_data.loc[general_info_data["name"] == key, "difficulty"].values.tolist()[0]


        read_data["name"] = key
        train_data_lst.append(read_data)           

train_data = pd.concat(train_data_lst)

cols = train_data.columns.to_list()

print(cols)
train_data = train_data.fillna(0)
cols.remove(target_col)
cols.remove("name")
cols.remove("time")

if correl:
    pear = "pearson"
    kend="kendall"
    spear="spearman"
    output = {pear:[],kend:[],spear:[]}
    all_data_out={}
    diagram_cols = []
    
    for val in cols:
        #print(val)
        x = train_data[val].corr(train_data[target_col], method=pear)
        y = train_data[val].corr(train_data[target_col], method=kend)
        z = train_data[val].corr(train_data[target_col], method=spear)
        print(x)
        all_data_out[val]={pear:x,kend:y,spear:z}

        com_val = 0.3
        if abs(x)>=com_val or abs(y)>=com_val or abs(z)>=com_val:
            output[pear].append(float("{:.4f}".format(x)))
            output[kend].append(float("{:.4f}".format(y)))
            output[spear].append(float("{:.4f}".format(z)))
            diagram_cols.append(val)
        print(val+":",x,y,z)

    # save correls
    pd.DataFrame(all_data_out).T.to_csv(f'{OUTPUT_PATH}correls_{FILE_PATH.split("_")[1]+"_"+FILE_PATH.split("_")[2][0]}_{mode.name}.csv')

    # draw diagram 
    fig, ax = plt.subplots(layout='constrained')
    x = np.arange(len(diagram_cols))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    for attribute, measurement in output.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Korrelation')
    ax.set_title(f'{mode.name}: Korrelation zwischen Messgrößen und {"gewichteter" if weighted else single_target_col} Belastung')
    ax.set_xticks(x + width, diagram_cols)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(-1,1)

    plt.show()

if anova:
    file_identifier = FILE_PATH.split("/")[1]
    good_cols = []
    all_data = train_data.fillna(0)
    all_data["name"] = all_data["name"].map(lambda x : x[:-1])
    print(all_data)
    anova_result = pd.DataFrame(columns=["col_name", "andat"])
    pairwise_result = pd.DataFrame()

    # calc ANOVA to get relevant sensors
    for col in cols:
        an_dat = pg.rm_anova( data = all_data,dv = col, within=target_col,subject = "name",detailed = True)
        if "p-unc" in an_dat.keys():
            value =an_dat["p-unc"].values.tolist()[0]
            anova_result = pd.concat([anova_result,pd.DataFrame({"col_name":[col], "andat":[value]})])
            if value < .05:
                good_cols.append(col)
                #print(col)
                #print(an_dat)
    print(anova_result)
    
    # save anova results
    anova_result.to_csv(path_or_buf=f"./{OUTPUT_PATH}/anova_res_{file_identifier}_{mode.name}.csv")

    # post toc test
    print(good_cols)
    for col in good_cols:

        pair_test = pg.pairwise_tests(data = all_data,dv = col,within = target_col,subject = "name", padjust = "bonf", effsize = "cohen")

        pair_test["column"] = col
        pairwise_result = pd.concat([pairwise_result,pair_test])
    # save results
    pairwise_result.to_csv(f"./{OUTPUT_PATH}/pairwise_{file_identifier}_{mode.name}.csv",columns=["column","A","B","p-unc","T","dof","alternative","p-corr","p-adjust","BF10","cohen"])
    print(pairwise_result)
