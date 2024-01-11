import pandas as pd 
import os
import json 
from  bokeh.plotting import figure,show,save,output_file
from bokeh.io import export_svg,export_png
from bokeh.models import ColumnDataSource
from matplotlib import pyplot as plt
from  const import const as c
import numpy as np
import seaborn as sns
from enum import Enum

def calc_weighted_target(data_file, user_name, target):
    
    print(raw_tlx_files)
    print(data_file)
    print(data_file.split("/")[-1])
    print(data_file.split("/")[-1].split(".")[0])
    user_name = data_file.split("/")[-1].split(".")[0].split("_")[0][:-1]
    task_type = data_file.split("/")[-1].split(".")[0].split("_")[1]

    user_data_path = "./data_processing/nutzerdaten.xlsx"
    user_data = pd.read_excel(user_data_path)
    user_data = user_data.loc[user_data["ID"] == user_name]
    print(user_data)

    workloads = []
    for key in target.keys():
        if task_type in key:
            workloads.append(target[key] * user_data[key.split("_")[1]].values.tolist()[0])
    x = sum(workloads)/3
    print(sum(workloads)/3)
    return x.values.tolist()[0]

COLORS = ["red", "blue", "green", "yellow", ]
class MODE (Enum):
    ALL = ["click","drag","phrase","write"]
    MOUSE = ["click","drag"]
    KEY = ["phrase","writing"]
    WRITE= ["writing"]
    PHRASE= ["phrase"]
    DRAG = ["drag"]
    CLICK =["click"]

    INFO = ["general"]

ORDER_DICT = {
    "a":[0,1,2],
    "b":[1,2,0],
    "c":[2,0,1],
    "d":[2,1,0],
    "e":[0,2,1],
    "f":[1,0,2],
}
keyboard_col = ["key_strokes","key_press_time","key_no_dead_time","key_dead_time_avg","key_deletions"]
mouse_col = ["mouse_avg_distance","mouse_avg_speed"]
analog = ["ana_max_travel","ana_total_time","ana_press_time","ana_press_vel","ana_hold_time","ana_release_time","ana_release_vel"]
eye = ["avg_size_left","max_size_left", "min_size_left","nan_pup_left","avg_size_right","max_size_right","min_size_right","nan_pup_right","avg_distance_right","avg_speed_right","avg_distance_left","avg_speed_left",]
# settings
mode = MODE.INFO

    # settings for INFO
SEPARAT = True
ALL_COMB = True
SINGLE_COL = True

    # settings for sensordata
columns = ["key_strokes"]
columns = ["avg_size_right" , "max_size_right","min_size_right","avg_size_left" , "max_size_left","min_size_left","ana_total_time","ana_press_time","ana_press_vel","ana_hold_time","ana_release_time","ana_release_vel"]
#columns = ["key_press_time"]

index_col = "time"
# import timeseries data
IMPORT_PATH = "./data_processing/processed_no_window/" # mit caps mit feac
#IMPORT_PATH = "./data_processing/processed___/" # ohne caps ohne feac
IMPORT_PATH = "./data_processing/processed_30_5apart/" # mit caps ohne feac
IMPORT_PATH = "./data_processing/processed_30_1apart/" # ohne caps mit feac
files = [f for f in os.listdir(IMPORT_PATH)]
tasks = ["writing", "phrase", "dragging", "clicking", "general"]
to_convert = ["key_press_time","key_dead_time_avg"]
sorted_files = {"general":[]}
raw_tlx_files = [file for file in os.listdir("./data_processing/all_data/") if "demand" in file] 
for f in files:
    split_str = f.split("_") 
    # 1. sort by user (safety) --> is also difficulty
    # 2. sort by task 
    if split_str[0] not in sorted_files.keys():
        sorted_files[split_str[0]]={x:[] for x in tasks}
    if "writing" in f:
        sorted_files[split_str[0]]["writing"].append(IMPORT_PATH+f)
    if "phrase" in f:
        sorted_files[split_str[0]]["phrase"].append(IMPORT_PATH+f)
    if "dragging" in f:
        sorted_files[split_str[0]]["dragging"].append(IMPORT_PATH+f)
    if "clicking" in f:
        sorted_files[split_str[0]]["clicking"].append(IMPORT_PATH+f)
    if "info" in f:
        sorted_files["general"].append(IMPORT_PATH+f)
#print(json.dumps(sorted_files, indent=2))

# use Info
if mode == MODE.INFO:
    ## read data
    gen_info = pd.concat([pd.read_csv(path) for path in sorted_files["general"]])
    gen_easy = gen_info.loc[gen_info["difficulty"] == 0]
    gen_middle = gen_info.loc[gen_info["difficulty"] == 1]
    gen_hard = gen_info.loc[gen_info["difficulty"] == 2]

    print(gen_info)
    # difficulty seperate
    if SEPARAT:
        diff_compare=[
            "phrase_levenshtein_sum_total",
            "phrase_levenshtein_avg_total",

            ]
        for col in diff_compare:
            meta = c[col]
            fig,ax = plt.subplots()
            x = pd.DataFrame({"keine":gen_easy[col].values,"0-Back":gen_middle[col].values,"1-Back":gen_hard[col].values})
            #gen_info.boxplot(column=["phrase_levenshtein_sum_total"])
            #x.boxplot(column=["Keine Sekundäraufgabe"])
            #print(x)
            print(c[col])
            ax.boxplot(x.values)
            for line in meta["extra_line"]:
                ax.axhline(y = line)
            ax.set_title(meta["title"])
            ax.set_ylabel(meta["y-title"])
            ax.set_xlabel("Sekundäraufgabe")
            ax.set_xticklabels(x.columns)
            plt.show()

    if ALL_COMB:
        columns=[
            "writing_word_sum",
            "writing_chars_space_sum",
            "writing_chars_nospace_sum",
            "phrase_word_sum",
            "phrase_chars_space_sum",
            "phrase_chars_nospace_sum",
        ]
        for col in columns:
            meta = c[col]
            fig,ax = plt.subplots()
            ax.boxplot(gen_info[col].dropna().values)
            for line in meta["extra_line"]:
                plt.axhline(y = line)
            ax.set_title(meta["title"])
            ax.set_ylabel(meta["y-title"])

            plt.show()

    if SINGLE_COL:
        columns = [                "clicking_total_res",
            #"clicking_total_nan",  
            "clicking_total_move",
            "dragging_total_res",
            "dragging_total_move"]
        for col in columns:
            meta = c[col]
            easy = gen_easy[col].value_counts()
            print(easy)
            x = sns.barplot(easy) 
            x.set_title(f"{meta['title']} (Keine Sekundäraufgabe)")
            x.set_ylabel(meta['y-title'])
            x.set_xlabel(meta['x-title'])
            plt.show()

            middle = gen_middle[col].value_counts()
            x = sns.barplot(middle) 
            x.set_title(f"{meta['title']} (0-Back)")
            x.set_ylabel(meta['y-title'])
            x.set_xlabel(meta['x-title'])
            plt.show()

            hard = gen_hard[col].value_counts()
            x = sns.barplot(hard) 
            x.set_title(f"{meta['title']} (1-Back)")
            x.set_ylabel(meta['y-title'])
            x.set_xlabel(meta['x-title'])
            plt.show()
else:
    data = pd.DataFrame(columns=columns + ["difficulty", "user"])
    gen_info = pd.concat([pd.read_csv(path) for path in sorted_files["general"]])
    print(sorted_files)
    print(gen_info)
    print(gen_info.columns)
    del sorted_files["general"]
    # select needed files

    for name, task_file_lists in sorted_files.items():
        print(name)
        print(name[-1])
        print(name[-5])
        difficulty = ORDER_DICT[name[-5]][int(name[-1])]
        for task in mode.value:
            if  task_file_lists[task]:

                if len(task_file_lists[task])>1:
                    read_data = pd.concat([pd.read_csv(file,usecols= columns+ [index_col]) for file in task_file_lists[task]])
                    
                else :
                    read_data = pd.read_csv(task_file_lists[task][0],usecols= columns + [index_col] )
                

                
                read_data["difficulty"] = 0
                if task not in MODE.WRITE.value:
                    print("richtige analyse ")
                    read_data["difficulty"] = difficulty
                #read_data["weight"] = calc_weighted_target(data_file = task_file_lists[task][0], user_name = name, target = pd.read_csv("./data_processing/all_data/"+[file for file in raw_tlx_files if name in file][0]))
                read_data["user"] = name[:-1]
                read_data[index_col] = pd.to_datetime(read_data[index_col])
                read_data[index_col] = (read_data[index_col] -read_data[index_col][0])/pd.Timedelta(seconds=1)
                print(read_data)
                data = pd.concat([data,read_data])
    
    for col in columns:
        
        if col in to_convert:
            data[col] = pd.to_timedelta(data[col])/pd.Timedelta(seconds=1)
        print(data)
        x = sns.FacetGrid(data, hue = "user",row = "difficulty")
        x.map(sns.lineplot,index_col,col)
        plt.show()