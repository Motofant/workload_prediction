import pandas as pd
import os
from key_mouse import KeyMouse
from analog import Analog
from eyetrack import EyeTrack
from text_processing import TextInfo
from mouse_processing import MouseProcess
import json
import numpy as np

# importpath ( all of it )

#logging_path = './logging/'
#logging_path = './example_only_keymouse/'
logging_path = './example_user/'
#logging_path = './logging/'
output_path = './processed_data'
files = [f for f in os.listdir(logging_path)]
tasks = ["writing", "phrase", "dragging", "clicking"]
key_mouse_sensor = "key_mouse"
analog_sensor = "analog"
eye_sensor = "eye"
sensors = [key_mouse_sensor,eye_sensor]
sensors = [key_mouse_sensor, analog_sensor, eye_sensor]
sorted_files = {}
for f in files:
    split_str = f.split("_") 
    # 1. sort by user (safety) --> is also difficulty
    # 2. sort by task 
    if split_str[0] not in sorted_files.keys():
        sorted_files[split_str[0]]={x:[] for x in tasks}
    if "writing" in f:
        sorted_files[split_str[0]]["writing"].append(logging_path+f)
    if "phrase" in f:
        sorted_files[split_str[0]]["phrase"].append(logging_path+f)
    if "dragging" in f:
        sorted_files[split_str[0]]["dragging"].append(logging_path+f)
    if "clicking" in f:
        sorted_files[split_str[0]]["clicking"].append(logging_path+f)

print(json.dumps(sorted_files, indent=2))

window_size = pd.Timedelta(seconds=2)
window_step = pd.Timedelta(seconds=1 )
init_ignore = pd.Timedelta(seconds=1) # no seconds ignored in the beginning 
general_info = pd.DataFrame()

for name in sorted_files.keys():
    if len(sorted_files[name]["writing"]) ==0:
        del sorted_files[name]["writing"]
    logging_path = logging_path + name
    user_info = {"name":name}
    # general 
        # Text
    if 'writing' in sorted_files[name].keys():
        gen_text = TextInfo(open([x for x in sorted_files[name]["writing"] if "user_entered" in x][0]).read(), None,  "writing_").output_dict()
        user_info.update(gen_text)
        # Phrase
    if "phrase" in sorted_files[name].keys():
        gen_phrase = TextInfo(
            compare_data = pd.read_csv([x for x in sorted_files[name]["phrase"] if "phrases" in x][0],header=None)[0].tolist(),
            user_data = pd.read_csv([x for x in sorted_files[name]["phrase"] if "user_entered" in x][0], index_col=[0],header=None)[1].tolist(),
            mode="phrase_",
            ).output_dict()
        user_info.update(gen_phrase)
        # Drag

    #if "dragging" in sorted_files[name].keys():
    #    gen_drag = MouseProcess(data=json.load(open([x for x in sorted_files[name]["dragging"] if "user_entered" in x][0])), mode = "dragging").output_dict()
    #    user_info.update(gen_drag)
    # Click
    if "clicking" in sorted_files[name].keys():
        gen_click = MouseProcess(data=json.load(open([x for x in sorted_files[name]["clicking"] if "user_entered" in x][0])), mode = "clicking").output_dict()
        user_info.update(gen_click)

    general_info = pd.concat([general_info,pd.DataFrame([user_info])])

    for task in sorted_files[name]:
        print(task)
        start_val = None
        end_val = None
        curr = None
        data_key = pd.DataFrame()
        data_ana = pd.DataFrame()
        data_eye = pd.DataFrame()
        task_out = pd.DataFrame()

        # reading files
        # key and mouse
        if key_mouse_sensor in sensors:
            data_key = pd.read_csv([x for x in sorted_files[name][task] if "key_mouse" in x][0], encoding="ISO-8859-1",quotechar='"',).set_index("time",drop=False)
            data_key.index = pd.to_datetime(data_key.index)
            data_key["time"] = pd.to_datetime(data_key["time"])
            # use as main timestamps 
            start_val = pd.to_datetime(data_key.iloc[0]["time"]) + init_ignore
            end_val = pd.to_datetime(data_key.iloc[-1]["time"])
            curr = start_val

        if analog_sensor in sensors:
            data_ana = pd.read_csv([x for x in sorted_files[name][task] if "analog" in x][0], 
                                encoding="ISO-8859-1",delimiter='|', 
                                dtype={ "perif":"string","location":int,"event":float,},
                                parse_dates=["time"],
                                skiprows=[1],
                                quotechar='"',
                                decimal=",",
                                ).set_index("time",drop=False) 
    
        if eye_sensor in sensors:
            data_eye = pd.read_csv([x for x in sorted_files[name][task] if "eye" in x][0],
                                encoding="ISO-8859-1",
                                quotechar='"',
                                dtype={"perif":str, "location":str, "value":object, },
                                ).set_index("time",drop=False)   
    
        while curr < end_val:

            task_temp_dict = {"time": curr}
            diff = curr + window_size

            if not data_key.empty:
                key = data_key.loc[(data_key["time"] >= curr) & (data_key["time"] < diff)]
                key_window = KeyMouse(key,window_size)
                task_temp_dict.update(key_window.out_dict())
            if not data_ana.empty:
                ana = data_ana.loc[(data_ana["time"] >= curr) & (data_ana["time"] < diff)]
                ana_window = Analog(ana)
                task_temp_dict.update(ana_window.output_dict())
            if not data_eye.empty:
                eye = data_eye.loc[(pd.to_datetime(data_eye["time"]) >= curr) & (pd.to_datetime(data_eye["time"]) < diff)]
                eye_window = EyeTrack(eye)
                task_temp_dict.update(eye_window.output_dict())
            task_out = pd.concat([task_out, pd.DataFrame([task_temp_dict])])
            print(curr)
            curr += window_step
        task_out.to_csv(f'{output_path}/{name}_{task}.csv', index=None)

general_info.to_csv(f'{output_path}/general_info.csv', index=None)

## Randnotzien
# Fenstergröße --> 30 sekunden
# fensterverschiebung --> 10 sekunden nach Startzeitpunkt (nicht erster wert) --> gleichförmiges Fenster