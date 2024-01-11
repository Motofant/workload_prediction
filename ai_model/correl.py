import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import seaborn as sns
from ai_constants import const as c 
import pingouin as pg
import math

# function
def calc_weighted_target(data_file, user_name, target):
    #print(data_file.split(".")[0].split("_")[0][:-1])
    user_name = data_file.split(".")[0].split("_")[0][:-1]
    task_type = data_file.split(".")[0].split("_")[1]

    user_data_path = "./nutzerdaten.xlsx"
    user_data = pd.read_excel(user_data_path)
    user_data = user_data.loc[user_data["ID"] == user_name]
    print("________")
    print(data_file)
    print(target)
    print(user_data)
    
    workloads = []
    for key in target.keys():
        if task_type in key:
            workloads.append(target[key] * user_data[key.split("_")[1]].values.tolist()[0])
    print( sum(workloads)/3)

    return sum(workloads)/3
    
def calc_mean_target(data_file,target):
    task_type = data_file.split(".")[0].split("_")[1]
    
    workloads = []
    for key in target.keys():
        if task_type in key:
            workloads.append(target[key])
    print(sum(workloads)/len(workloads))
    return sum(workloads)/len(workloads)

# constants
to_convert = ["key_press_time","key_dead_time_avg"]
rename = {0:"keine",1:"0-Back", 2:"1-Back"}
single_target_col = "_mental"
target_col = "goal"
train_data = pd.DataFrame()
test_data = pd.DataFrame()
workload_mean = pd.DataFrame()

class MODE (Enum):
    ALL = ["click","drag","phrase","write"]
    REPEATED = ["click","drag","phrase"]
    MOUSE = ["click","drag"]
    KEY = ["phrase","writing"]
    WRITE= ["writing"]
    PHRASE= ["phrase"]
    DRAG = ["drag"]
    CLICK =["click"]

# variables
## target type
weighted = True
mean = False
categorical = False
workload_level = False
weight_to_work = False

## mode 
mode = MODE.CLICK


## statistics0
correl = True
box_plot = False
stat_analysis = False

# import path 

FILE_PATH = "./processed_2_1apart/"
#FILE_PATH = "./processed_30_5apart/"
#FILE_PATH = "./processed_no_window/"


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


print(sorted_files)
print(workload_mean.shape)
# startt labeling
for key,lst in sorted_files.items():

    target = pd.read_csv(FILE_PATH+label[key]).to_dict(orient="records")[0]
    
    #print(target)
    # get demands
    for i in lst:
        read_data = pd.read_csv(FILE_PATH+i).fillna(0)
        read_data = read_data.replace("NaN",0)
        if workload_mean.shape[1] == 0:
            workload_mean = pd.DataFrame(columns= read_data.columns)
        for val in to_convert:
            read_data[val] = pd.to_timedelta(read_data[val])/pd.Timedelta(seconds=1)

        # get target column
        if weighted:
            read_data[target_col] = calc_weighted_target(data_file = i, user_name = key, target = target)
            read_data["name"] = key
            #print(read_data[target_col])
        elif mean:
            read_data[target_col] = calc_mean_target(data_file = i, target = target)
        else:
            read_data[target_col] = target[i.split(".")[0].split("_")[1] + single_target_col]/20
        if categorical: 
            read_data[target_col]=read_data[target_col].apply(lambda value: 0 if value <33 else (1 if value < 66 else 2 )) 
            #read_data[target_col] = 2 if read_data[target_col] >66 else 1 if read_data[target_col] >33 else 0
        if workload_level:
            read_data[target_col] = rename[general_info_data.loc[general_info_data["name"] == key, "difficulty"].values.tolist()[0]]
            read_data[target_col] = general_info_data.loc[general_info_data["name"] == key, "difficulty"].values.tolist()[0]
            read_data["name"] = key
            workload_mean = pd.concat([workload_mean,read_data])

        if weight_to_work:
            read_data["weight"]=calc_weighted_target(data_file = i, user_name = key, target = target)
            
            read_data[target_col] = rename[general_info_data.loc[general_info_data["name"] == key, "difficulty"].values.tolist()[0]]
            read_data[target_col] = general_info_data.loc[general_info_data["name"] == key, "difficulty"].values.tolist()[0]

            workload_mean = pd.concat([workload_mean,read_data])           

        

        # 90% trianing 10% test
        length = int(read_data.shape[0]*1)
        if train_data.shape[0] != 0:

            train_data = pd.concat([train_data, read_data.iloc[:length]])
            test_data = pd.concat([test_data,read_data.iloc[length:]])
            
        else:
            train_data = read_data.iloc[:length]
            test_data = read_data.iloc[length:]               

if workload_level or weight_to_work:
    train_data = workload_mean
    if weight_to_work:
        train_data = train_data.loc[:,["time","weight","name",target_col]]
    cols = train_data.columns.to_list()
    print(cols)

else:
    cols = train_data.columns.to_list()

print(cols)
train_data = train_data.fillna(0)
cols.remove("goal")
cols.remove("name")
cols.remove("time")

if correl:
    pear = "pearson"
    kend="kendall"
    spear="spearman"
    output = {pear:[],kend:[],spear:[]}
    diagram_cols = []
    print(train_data)
    
    #del cols[0]
    for val in cols:
        #print(val)
        x = train_data[val].corr(train_data[target_col], method="pearson")
        y = train_data[val].corr(train_data[target_col], method="kendall")
        z = train_data[val].corr(train_data[target_col], method="spearman")
        com_val = 0.3
        if abs(x)>=com_val or abs(y)>=com_val or abs(z)>=com_val:
            output[pear].append(float("{:.4f}".format(x)))
            output[kend].append(float("{:.4f}".format(y)))
            output[spear].append(float("{:.4f}".format(z)))
            diagram_cols.append(val)
        print(val+":",x,y,z)

    # gen diagramm
    x = np.arange(len(diagram_cols))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

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

if box_plot:
    cat = "Sekundäraufgabe"
    #rename = {0:"keine",1:"0-Back", 2:"1-Back"}
    #general_info = pd.read_csv(FILE_PATH + "general_info.csv")
    print(cols)
    for col in cols:
        data = train_data.loc[:,[col,target_col]]
        print("data ",data)
        #meta = c[col]
        x = sns.boxplot(data= data, x = target_col,y = col,order= rename.values())
        x.set_title(f"{mode.name}: {c[col]['name']}")
        x.set_ylabel(f"{c[col]['y_name']}")
        plt.show()

if stat_analysis:
    ttest = True
    correls = False
    normal = False
    anova = False

    ttest_data = {}
    correl_data = {}
    normal_data = {}
    anova_goal_data = {}
    anova_within_data = {}
    print(train_data)
    for col in cols:
        print(col)
        # t-Test
        if ttest:
            
            ttest_res = pg.ttest(train_data.loc[:,col],train_data[target_col])
            x = ttest_res["p-val"].values
            #print(type(x))
            #print(x)
            if x:
                print("x works")
            if pd.isnull(x):
                print("insnan")
            if not pd.isnull(x):

                if abs(x) > .1 : 
                    ttest_data[col] = x
            #print(ttest_res["p-val"].values)

        if correls:
        # correlation
            print(train_data.loc[:,col])
            corr_res = pg.corr(train_data.loc[:,col],train_data[target_col])
            #print(corr_res["r"].values)
            x = corr_res["r"].values
            if not pd.isnull(x):
                if abs(x) > .15:
                    correl_data[col] = x 
        
        if normal:
            pass 

        if anova:
            #print("start anova")
            print(train_data.head())
            train_data = train_data.fillna(0)
            an_dat = pg.rm_anova( data = train_data,dv = col, within=target_col,subject = "name",detailed = False)
            print(an_dat)
            if "np2" in an_dat:
                x = an_dat["np2"].values
                if not pd.isnull(x):
                    if abs(x) > .03:
                        print(x)
                        anova_goal_data[col] = x
                    
    if ttest:
        x = sns.barplot(ttest_data)
        for i in x.containers:
            x.bar_label(i,)
        x.set_title("T-Test: p-val")
        #print(ttest_data)
        plt.show()
    if correls:
        print(correl_data)
        x = sns.barplot(correl_data)
        x.set_title("Pearson Korrelation: r-Wert")
        for i in x.containers:
            x.bar_label(i,)
        #print(ttest_data)
        plt.show()
    if anova:
        x = sns.barplot(anova_goal_data)
        x.set_title("Anova: Partial Eta Squared")
        for i in x.containers:
            x.bar_label(i,)
        #print(ttest_data)
        plt.show()
    if normal:
        pass
