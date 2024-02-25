from enum import Enum
import pandas as pd 

# classes
class MODE (Enum):
    ALL = ["click","drag","phrase","writing"]
    NBACK = ["click","drag","phrase",]
    MOUSE = ["click","drag"]
    KEY = ["phrase","writing"]
    WRITE= ["writing"]
    PHRASE= ["phrase"]
    DRAG = ["drag"]
    CLICK =["click"]

class MODELS (Enum):
    RF_REG = {
        "model":"rf",
        "mode":"regression",
        "classes":0,
        }
    RF_CLASS_2={
        "model":"rf",
        "mode":"classification",
        "classes":2,
    }
    RF_CLASS_3={
        "model":"rf",
        "mode":"classification",
        "classes":3,
    }
# functions
def get_relevant_metrics(mode,small_window,weighted):
    cols = []
    if mode == "DRAG":
        if weighted:
            col_base = ["avg_size_right","max_size_left","max_size_right"]
            col_extend =  ["min_size_right"] if small_window else ["avg_size_left"]
            cols = col_base + col_extend
        else:
            col_base = ["avg_size_left","avg_size_right","max_size_left","max_size_right","avg_speed_right"]
            col_extend = ["min_size_right","min_size_left","avg_speed_left","avg_distance_left","avg_distance_right","mouse_avg_distance","mouse_avg_speed"] if small_window else [] 
            cols = col_base + col_extend
    elif mode == "CLICK" :
        if weighted:
            col_base = ["avg_size_left","avg_size_right","max_size_left","max_size_right"]
            col_extend =  ["min_size_right","min_size_left"] if small_window else ["mouse_avg_distance","mouse_avg_speed"]
            cols = col_base + col_extend
        else:
            col_base = ["avg_size_left","avg_size_right","max_size_left","max_size_right"]
            col_extend = ["min_size_right","min_size_left"] if small_window else [] 
            cols = col_base + col_extend
    elif mode == "MOUSE": 
        if weighted:
            col_base = ["avg_size_left","avg_size_right","max_size_left","max_size_right"]
            col_extend =  ["min_size_right"] if small_window else ["mouse_avg_distance","mouse_avg_speed"]
            cols = col_base + col_extend
        else:
            col_base = ["avg_size_left","avg_size_right","max_size_left","max_size_right","min_size_right","nan_pup_left","mouse_avg_speed"]
            col_extend = ["min_size_left","avg_speed_left","avg_speed_right", "mouse_avg_distance"] if small_window else [] 
            cols = col_base + col_extend
    elif mode == "PHRASE" :
        if weighted:
            col_base = ["avg_size_left","avg_size_right","max_size_left","max_size_right"]
            col_extend =  [] if small_window else []
            cols = col_base + col_extend
        else:
            col_base = ["key_strokes","avg_size_left","avg_size_right","max_size_left","max_size_right","ana_total_time","key_dead_time_avg","key_no_dead_time","ana_press_time","nan_pup_right","nan_pup_left","key_press_time",]
            col_extend = ["min_size_left","ana_press_vel","ana_release_time","ana_hold_time",] if small_window else ["ana_release_vel","min_size_right",] 
            cols = col_base + col_extend
    elif mode == "WRITE":
        cols = ["key_no_dead_time","ana_max_travel","ana_release_vel","max_size_left","max_size_right","nan_pup_right","nan_pup_left","min_size_right",]  
        if weighted:
            col_base = ["nan_pup_right","nan_pup_left","ana_max_travel","ana_release_time","ana_release_vel",]
            col_extend =  [] if small_window else ["key_no_dead_time","key_dead_time_avg","max_size_left","max_size_right","min_size_right","avg_size_right",]
            cols = col_base + col_extend
        else:
            # Cant be used for categorising --> no classes
            col_base = []
            col_extend = [] if small_window else [] 
            cols = col_base + col_extend
    elif mode == "KEY":
        if weighted:
            col_base = []
            col_extend =  [] if small_window else ["ana_hold_time", "avg_size_right",]
            cols = col_base + col_extend
        else:
            # Cant be used for categorising --> no classes in "WRITE"-task
            col_base = []
            col_extend = [] if small_window else [] 
            cols = col_base + col_extend
    elif mode == "ALL":
        cols = ["key_strokes","key_no_dead_time","key_dead_time_avg","avg_size_left","max_size_left","nan_pup_left","avg_size_right","max_size_right","min_size_right","nan_pup_right","ana_total_time","ana_press_time","ana_release_vel",]
        if weighted:
            col_base = ["avg_size_right","max_size_right",]
            col_extend =  [] if small_window else ["max_size_left","avg_size_left",]
            cols = col_base + col_extend
        else:
            # Cant be used for categorising --> no classes in "WRITE"-task
            col_base = []
            col_extend = [] if small_window else [] 
            cols = col_base + col_extend
    elif mode == "NBACK":
        if weighted:
            col_base = ["mouse_avg_distance","mouse_avg_speed","avg_size_left","avg_size_right","max_size_left","max_size_right",]
            col_extend =  [] if small_window else ["ana_release_vel","ana_press_vel","ana_max_travel"]
            cols = col_base + col_extend
        else:
            col_base = ["avg_size_left","avg_size_right","max_size_left","max_size_right","key_strokes","key_no_dead_time","key_dead_time_avg","min_size_left","min_size_right","nan_pup_left","nan_pup_right","avg_speed_left","avg_speed_right",] #13
            col_extend = ["ana_press_time","ana_press_vel","ana_total_time","mouse_avg_distance","mouse_avg_speed","key_press_time","ana_release_time"] if small_window else ["ana_release_vel"] 
            cols = col_base + col_extend
    
    return cols

## calculate targetcolum
def calc_weighted_target(data_file, target):
    # claculating NASA-TLX value from 
    #print(data_file.split(".")[0].split("_")[0][:-1])
    user_name = data_file.split(".")[0].split("_")[0][:-1]
    task_type = data_file.split(".")[0].split("_")[1]

    user_data_path = "./nutzerdaten_anon.xlsx"
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

