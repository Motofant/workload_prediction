import pandas as pd
import os
from key_mouse import KeyMouse
from analog import Analog
import json

# import data ( all of it )
logging_path = './logging/'
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

window_size = pd.Timedelta(seconds=30)
window_step = pd.Timedelta(seconds=10)

for name in sorted_files.keys():
    #filerreading
    data_write_key = pd.read_csv([x for x in sorted_files[name]["writing"] if "key_mouse" in x][0], encoding="ISO-8859-1").set_index("time",drop=False)
    data_write_ana = pd.read_csv([x for x in sorted_files[name]["writing"] if "analog" in x][0], 
                                encoding="ISO-8859-1",delimiter='|', 
                                dtype={ "perif":"string","location":int,"event":float,},
                                parse_dates=["time"],
                                skiprows=[1],
                                decimal=","
                                ).set_index("time",drop=False)
    print(len(data_write_ana))
    #data_write_eye = pd.read_csv([x for x in sorted_files[name]["writing"] if "eye" in x][0], encoding="ISO-8859-1").set_index("time",drop=False)

    #data_phrase_key = pd.read_csv([x for x in sorted_files[name]["phrase"] if "key_mouse" in x][0], encoding="ISO-8859-1").set_index("time",drop=False)
    #data_drag_key = pd.read_csv([x for x in sorted_files[name]["dragging"] if "key_mouse" in x][0], encoding="ISO-8859-1").set_index("time",drop=False)
    #data_click_key = pd.read_csv([x for x in sorted_files[name]["clicking"] if "key_mouse" in x][0], encoding="ISO-8859-1").set_index("time",drop=False)

    # writing
    start_val =pd.to_datetime(data_write_key.iloc[0]["time"])
    end_val =pd.to_datetime(data_write_key.iloc[-1]["time"])
    data_write_key = data_write_key.set_index("time",drop=False)
    data_write_key.index = pd.to_datetime(data_write_key.index)
    data_write_key["time"] = pd.to_datetime(data_write_key["time"])
    curr = start_val
    print(start_val)
    output = pd.DataFrame()
    # rolling window
    while curr < end_val:
        # get start and end
        diff = curr + window_size

        # get data from every log
        key = data_write_key.loc[(data_write_key["time"] >= curr) & (data_write_key["time"] < diff)]
        ana = data_write_ana.loc[(data_write_ana["time"] >= curr) & (data_write_ana["time"] < diff)]
        #eye = data_write_eye.loc[(data_write_eye["time"] >= curr) & (data_write_eye["time"] < diff)]
        key_window = KeyMouse(key,window_size)
        #key_window.output_string()
        ana_window = Analog(ana)

        out_dict = {"time": curr,**ana_window.output_dict(),}
        print(out_dict)
        output = pd.concat([output, pd.DataFrame([out_dict])])
        curr += window_step
        print(curr)
    output = output.set_index(pd.DatetimeIndex(output["time"])).drop("time",axis=1)
    print(output)
exit(1)
path = "./test.log"

fct = lambda x : print(x)
#data_analog = pd.read_csv(path_ana, delimiter= "|")
data_total = pd.read_csv(path, encoding="ISO-8859-1")

start_val =pd.to_datetime(data_total.iloc[0]["time"])
end_val =pd.to_datetime(data_total.iloc[-1]["time"])
data_total = data_total.set_index("time",drop=False)
data_total.index = pd.to_datetime(data_total.index)
data_total["time"] = pd.to_datetime(data_total["time"])

curr = start_val



# rolling window
while curr < end_val:
    # get start and end
    diff = curr + window_size

    # get data from every log
    x = data_total.loc[(data_total["time"] >= curr) & (data_total["time"] < diff)]
    y = KeyMouse(x,window_size)
    y.output_string()
    curr += window_step
    #print(pd.to_datetime(x.iloc[-1]["time"])-pd.to_datetime(x.iloc[0]["time"]))

## Randnotzien
# Fenstergröße --> 30 sekunden
# fensterverschiebung --> 10 sekunden nach Startzeitpunkt (nicht erster wert) --> gleichförmiges Fenster