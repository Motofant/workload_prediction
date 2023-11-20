import pandas as pd 
import os
import json 
from  bokeh.plotting import figure,show,save,output_file
from bokeh.io import export_svg,export_png
from bokeh.models import ColumnDataSource
import numpy as np
# import timeseries data
IMPORT_PATH = "./data_processing/processed_data/"
files = [f for f in os.listdir(IMPORT_PATH)]
tasks = ["writing", "phrase", "dragging", "clicking", "info"]
sorted_files = {}
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
        sorted_files[split_str[0]]["info"].append(IMPORT_PATH+f)
#print(json.dumps(sorted_files, indent=2))
#open([x for x in sorted_files[name]["writing"] if "user_entered" in x][0]).read()

relevant_cols = ["time","key_strokes","key_press_time","avg_size_right" , "max_size_right","min_size_right","avg_size_left" , "max_size_left","min_size_left","ana_total_time","ana_press_time","ana_press_vel","ana_hold_time","ana_release_time","ana_release_vel"]
COLORS=["red","orange","green"]
task = "phrase"
val = "key_strokes"
to_convert = ["key_press_time","key_dead_time_avg"]
wait = ["key_strokes","key_press_time","avg_size_right" , "max_size_right","min_size_right","avg_size_left" , "max_size_left","min_size_left","ana_total_time","ana_press_time","ana_press_vel","ana_hold_time","ana_release_time","ana_release_vel"]
for val in wait:#["key_press_time","ana_total_time","ana_press_time","ana_press_vel","ana_hold_time","ana_release_time","ana_release_vel"]:
    p = figure(
        title=f"{task}: {val}", 
        x_axis_type="datetime",
        )

    for i, name in enumerate(["studefabdc0","studefabdc1","studefabdc2"]):#enumerate(["karian1","karian2","karian3"]):
        data = pd.read_csv(sorted_files[name][task][0])
        data["time"] = pd.to_datetime(data["time"])
        data["time"] = data["time"] -data["time"][0]
        data["color"] = COLORS[i]
        
        if val in to_convert:
            data[val] = pd.to_timedelta(data[val])/pd.Timedelta(seconds=1)
            #print(data[val])
        
        relevant_cols += ["color"]
        col_dat_src = ColumnDataSource(data= data.loc[:,relevant_cols])
        p.line(x =relevant_cols[0],y=val,color = COLORS[i], line_width=2,source = col_dat_src,legend_label=f"{val}: {name}")
    out_file  = output_file(filename=f"./data_processing/output_diagramm/{task}_{val}.png")
    export_png(p, filename=f"./data_processing/output_diagramm/{task}_{val}.png")
    #show(p)
    #save (p)
    #export_svg(obj= p,filename=f"./{task}_{val}.html")
'''
for name in ["karian1","karian2","karian3"]:
    for task, lst in sorted_files[name].items():
        if len(lst) == 1 and task == "phrase":
            data = pd.read_csv(lst[0])#, index_col="time")
            data["time"] = pd.to_datetime(data["time"])
            data["time"] = data["time"] -data["time"][0]
            print(data)

            print(data.loc[:,"key_strokes"])
#            print(data.loc[:,"key_strokes"])
            col_dat_src = ColumnDataSource(data= data.loc[:,relevant_cols])
            print(col_dat_src)
            #p.line(x = "time",y="key_strokes",source = col_dat_src)
            for col in relevant_cols[1:]:
                p.line(x =relevant_cols[0],y=col, source = col_dat_src,legend_label=col)
            p.legend.location = "top_left"
            show(p)'''