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
## target type --> NOT WORKING
weighted = False
mean = False
categorical = False
workload_level = False
weight_to_work = False

## mode 
mode = MODE.PHRASE

## statistics0
correl = False
box_plot = False
stat_analysis = True

# import path 
FILE_PATH = "./processed_2_1apart/"
#FILE_PATH = "./processed_30_5apart/"
#FILE_PATH = "./processed_no_window/"

file_identifier = FILE_PATH.split("/")[1]
print(file_identifier)

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

#print(sorted_files)
all_data = pd.DataFrame()
nameID = 0
for name, files in sorted_files.items():
    loads = pd.read_csv(FILE_PATH+label[name]).to_dict(orient="records")[0]
    for file in files:
        # read data
        read_data = pd.read_csv(FILE_PATH+file).fillna(0)
        read_data = read_data.replace("NaN",0)
        del read_data["time"]
        for val in to_convert:
            read_data[val] = pd.to_timedelta(read_data[val])/pd.Timedelta(seconds=1)
        read_data = read_data.mean().to_frame().T
        read_data["name"] = name#[:-1]
        read_data[target_col] = rename[general_info_data.loc[general_info_data["name"] == name, "difficulty"].values.tolist()[0]]
        read_data[target_col] = general_info_data.loc[general_info_data["name"] == name, "difficulty"].values.tolist()[0]
        if all_data.empty:
            all_data=read_data

        else:

            all_data=pd.concat([all_data,read_data])
        #print(name, read_data[target_col])
    nameID += 1
print(all_data)
cols = all_data.columns.to_list()
cols.remove("goal")
cols.remove("name")
good_cols = []
all_data = all_data.fillna(0)
all_data["name"] = all_data["name"].map(lambda x : x[:-1])
all_data.to_csv("./hallo.csv")
anova_result = pd.DataFrame(columns=["col_name", "andat"])
pairwise_result = pd.DataFrame()
for col in cols:
    print(col)
    print(target_col)
    an_dat = pg.rm_anova( data = all_data,dv = col, within=target_col,subject = "name",detailed = True)
    print(an_dat)
    exit(1)
    if "p-unc" in an_dat.keys():
        value =an_dat["p-unc"].values.tolist()[0]
        anova_result = pd.concat([anova_result,pd.DataFrame({"col_name":[col], "andat":[value]})])
        if value < .05:
            good_cols.append(col)
            #print(col)
            #print(an_dat)
print(anova_result)
anova_result.to_csv(path_or_buf=f"./anova_result/anova_res_{file_identifier}_{mode.name}.csv")
# post toc test
print(good_cols)
for col in good_cols:
    print(col)
    pair_test = pg.pairwise_tests(data = all_data,dv = col,within = target_col,subject = "name", padjust = "bonf", effsize = "cohen")
    print(pair_test)
    pair_test["column"] = col
    pairwise_result = pd.concat([pairwise_result,pair_test])
pairwise_result.to_csv(f"./anova_result/pairwise_{file_identifier}_{mode.name}.csv",columns=["column","A","B","p-unc","T","dof","alternative","p-corr","p-adjust","BF10","cohen"])
print(pairwise_result)