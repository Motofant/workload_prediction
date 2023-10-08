import pandas as pd
import os
from key_mouse import KeyMouse
from analog import Analog
from eyetrack import EyeTrack
from text_processing import TextInfo
from mouse_processing import MouseProcess
import json
import numpy as np

# import data ( all of it )
#logging_path = './logging/'
logging_path = './example_only_keymouse/'

output_path = './processed_data'
files = [f for f in os.listdir(logging_path)]
tasks = ["writing", "phrase", "dragging", "clicking"]
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

window_size = pd.Timedelta(seconds=10)
window_step = pd.Timedelta(seconds=2)
general_info = pd.DataFrame()
for name in sorted_files.keys():
    if len(sorted_files[name]["writing"]) ==0:
        del sorted_files[name]["writing"]
    logging_path = logging_path + name
    # general 
        # Text
    if 'writing' in sorted_files[name].keys():
        gen_text = TextInfo(open([x for x in sorted_files[name]["writing"] if "user_entered" in x][0]).read(), None,  "writing_").output_dict()
        # Phrase
    gen_phrase = TextInfo(
        compare_data = pd.read_csv([x for x in sorted_files[name]["phrase"] if "phrases" in x][0],header=None)[0].tolist(),
        user_data = pd.read_csv([x for x in sorted_files[name]["phrase"] if "user_entered" in x][0], index_col=[0],header=None)[1].tolist(),
        mode="Phrase_",
        ).output_dict()
        # Drag
    gen_drag = MouseProcess(data=json.load(open([x for x in sorted_files[name]["dragging"] if "user_entered" in x][0])), mode = "dragging").output_dict()
        # Click
    gen_click = MouseProcess(data=json.load(open([x for x in sorted_files[name]["clicking"] if "user_entered" in x][0])), mode = "clicking").output_dict()
    x = {"name":name, **gen_text,**gen_phrase,**gen_drag,**gen_click}

    general_info = pd.concat([general_info,pd.DataFrame([x])])

    #filerreading
    if 'writing' in sorted_files[name].keys():
        
        data_write_key = pd.read_csv([x for x in sorted_files[name]["writing"] if "key_mouse" in x][0], encoding="ISO-8859-1",quotechar='"',).set_index("time",drop=False)
        print(data_write_key)
        data_write_ana = pd.read_csv([x for x in sorted_files[name]["writing"] if "analog" in x][0], 
                                    encoding="ISO-8859-1",delimiter='|', 
                                    dtype={ "perif":"string","location":int,"event":float,},
                                    parse_dates=["time"],
                                    skiprows=[1],
                                    quotechar='"',
                                    decimal=",",
                                    ).set_index("time",drop=False)
        data_write_eye = pd.read_csv([x for x in sorted_files[name]["writing"] if "eye" in x][0],
                                    encoding="ISO-8859-1",
                                    quotechar='"',
                                    dtype={"perif":str, "location":str, "value":object,},
                                    ).set_index("time",drop=False)
        print(len(data_write_ana))
        #data_write_eye = pd.read_csv([x for x in sorted_files[name]["writing"] if "eye" in x][0], encoding="ISO-8859-1").set_index("time",drop=False)

    data_phrase_key = pd.read_csv([x for x in sorted_files[name]["phrase"] if "key_mouse" in x][0], encoding="ISO-8859-1",quotechar='"',).set_index("time",drop=False)
    data_phrase_ana = pd.read_csv([x for x in sorted_files[name]["phrase"] if "analog" in x][0], 
                                encoding="ISO-8859-1",delimiter='|', 
                                dtype={ "perif":"string","location":int,"event":float,},
                                parse_dates=["time"],
                                skiprows=[1],
                                quotechar='"',
                                decimal=",",
                                ).set_index("time",drop=False)    
    data_phrase_eye = pd.read_csv([x for x in sorted_files[name]["phrase"] if "eye" in x][0],
                                encoding="ISO-8859-1",
                                quotechar='"',
                                dtype={"perif":str, "location":str, "value":object, },
                                ).set_index("time",drop=False)

    data_drag_key = pd.read_csv([x for x in sorted_files[name]["dragging"] if "key_mouse" in x][0], encoding="ISO-8859-1",quotechar='"',).set_index("time",drop=False)   
    data_drag_eye = pd.read_csv([x for x in sorted_files[name]["dragging"] if "eye" in x][0],
                                encoding="ISO-8859-1",
                                quotechar='"',
                                dtype={"perif":str, "location":str, "value":object},
                                ).set_index("time",drop=False)
    
    data_click_key = pd.read_csv([x for x in sorted_files[name]["clicking"] if "key_mouse" in x][0], encoding="ISO-8859-1").set_index("time",drop=False)
    data_click_eye = pd.read_csv([x for x in sorted_files[name]["clicking"] if "eye" in x][0],
                                encoding="ISO-8859-1",
                                quotechar='"',
                                dtype={"perif":str, "location":str, "value":object},
                                ).set_index("time",drop=False)
    
    # writing
    start_val =pd.to_datetime(data_write_key.iloc[0]["time"])
    end_val =pd.to_datetime(data_write_key.iloc[-1]["time"])
    data_write_key = data_write_key.set_index("time",drop=False)
    data_write_key.index = pd.to_datetime(data_write_key.index)
    data_write_key["time"] = pd.to_datetime(data_write_key["time"])
    curr = start_val
    print(start_val)
    writing_out = pd.DataFrame()
    # rolling window
    while curr < end_val:
        # get start and end
        diff = curr + window_size

        # get data from every log
        key = data_write_key.loc[(data_write_key["time"] >= curr) & (data_write_key["time"] < diff)]
        ana = data_write_ana.loc[(data_write_ana["time"] >= curr) & (data_write_ana["time"] < diff)]
        #eye = data_write_eye.loc[(pd.to_datetime(data_write_eye["time"]) >= curr) & (pd.to_datetime(data_write_eye["time"]) < diff)]
        
        key_window = KeyMouse(key,window_size)
        ana_window = Analog(ana)
        #eye_window = EyeTrack(eye)

        write_out_dict = {"time": curr,**ana_window.output_dict(),**key_window.out_dict(), }#**eye_window.output_dict()}
        print(write_out_dict)
        writing_out = pd.concat([writing_out, pd.DataFrame([write_out_dict])])
        curr += window_step
        print(curr)
    writing_out = writing_out.set_index(pd.DatetimeIndex(writing_out["time"])).drop("time",axis=1)
    writing_out.to_csv(f'{output_path}/{name}_writing.csv')
    
    # phrase
    start_val =pd.to_datetime(data_phrase_key.iloc[0]["time"])
    end_val =pd.to_datetime(data_phrase_key.iloc[-1]["time"])
    data_phrase_key = data_phrase_key.set_index("time",drop=False)
    data_phrase_key.index = pd.to_datetime(data_phrase_key.index)
    data_phrase_key["time"] = pd.to_datetime(data_phrase_key["time"])
    curr = start_val
    print(start_val)
    phrase_out = pd.DataFrame()
    # rolling window
    while curr < end_val:
        # get start and end
        diff = curr + window_size

        # get data from every log
        key = data_phrase_key.loc[(data_phrase_key["time"] >= curr) & (data_phrase_key["time"] < diff)]
        ana = data_phrase_ana.loc[(data_phrase_ana["time"] >= curr) & (data_phrase_ana["time"] < diff)]
        #eye = data_phrase_eye.loc[(pd.to_datetime(data_phrase_eye["time"]) >= curr) & (pd.to_datetime(data_phrase_eye["time"]) < diff)]

        key_window = KeyMouse(key,window_size)
        ana_window = Analog(ana)
        #eye_window = EyeTrack(eye)

        phrase_out_dict = {"time": curr,**ana_window.output_dict(),**key_window.out_dict(), }#**eye_window.output_dict()}
        print(phrase_out_dict)
        phrase_out = pd.concat([phrase_out, pd.DataFrame([phrase_out_dict])])
        curr += window_step
        print(curr)
    
    phrase_out = phrase_out.set_index(pd.DatetimeIndex(phrase_out["time"])).drop("time",axis=1)
    phrase_out.to_csv(f'{output_path}/{name}_phrasing.csv')
    
    # dragging
    start_val =pd.to_datetime(data_drag_key.iloc[0]["time"])
    end_val =pd.to_datetime(data_drag_key.iloc[-1]["time"])
    data_drag_key = data_drag_key.set_index("time",drop=False)
    data_drag_key.index = pd.to_datetime(data_drag_key.index)
    data_drag_key["time"] = pd.to_datetime(data_drag_key["time"])
    curr = start_val
    print(start_val)
    drag_out = pd.DataFrame()
    # rolling window
    while curr < end_val:
        # get start and end
        diff = curr + window_size

        # get data from every log
        key = data_drag_key.loc[(data_drag_key["time"] >= curr) & (data_drag_key["time"] < diff)]
        #eye = data_drag_eye.loc[(pd.to_datetime(data_drag_eye["time"]) >= curr) & (pd.to_datetime(data_drag_eye["time"]) < diff)]
        key_window = KeyMouse(key,window_size)
        #eye_window = EyeTrack(eye)
        drag_out_dict = {"time": curr,**key_window.out_dict(),}# **eye_window.output_dict()}
        print(drag_out_dict)
        drag_out = pd.concat([drag_out, pd.DataFrame([drag_out_dict])])
        curr += window_step
    drag_out = drag_out.set_index(pd.DatetimeIndex(drag_out["time"])).drop("time",axis=1)
    drag_out.to_csv(f'{output_path}/{name}_dragging.csv')

    # clicking
    start_val =pd.to_datetime(data_click_key.iloc[0]["time"])
    end_val =pd.to_datetime(data_click_key.iloc[-1]["time"])
    data_click_key = data_click_key.set_index("time",drop=False)
    data_click_key.index = pd.to_datetime(data_click_key.index)
    data_click_key["time"] = pd.to_datetime(data_click_key["time"])
    curr = start_val
    print(start_val)
    click_out = pd.DataFrame()
    # rolling window
    while curr < end_val:
        # get start and end
        diff = curr + window_size

        # get data from every log
        key = data_click_key.loc[(data_click_key["time"] >= curr) & (data_click_key["time"] < diff)]
        #eye = data_click_eye.loc[(pd.to_datetime(data_click_eye["time"]) >= curr) & (pd.to_datetime(data_click_eye["time"]) < diff)]
        key_window = KeyMouse(key,window_size)
        #eye_window = EyeTrack(eye)
        click_out_dict = {"time": curr,**key_window.out_dict(),}# **eye_window.output_dict()}
        print(click_out_dict)
        click_out = pd.concat([click_out, pd.DataFrame([click_out_dict])])
        curr += window_step
    click_out = click_out.set_index(pd.DatetimeIndex(click_out["time"])).drop("time",axis=1)
    click_out.to_csv(f'{output_path}/{name}_clicking.csv')
general_info.to_csv(f'{output_path}/general_info.csv', index=None)
## Randnotzien
# Fenstergröße --> 30 sekunden
# fensterverschiebung --> 10 sekunden nach Startzeitpunkt (nicht erster wert) --> gleichförmiges Fenster