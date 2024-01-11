# imports 
import joblib
import subprocess
import psutil
import sys
import pandas as pd
from data_processing.key_mouse import KeyMouse
from datetime import datetime as dt
import numpy as np
# fct
def getRF():
    return joblib.load(weights["rf"])

def get_data(window):
    # get all data
    data = pd.read_csv("./logging/test_test_key_mouse_logging.log", encoding="ISO-8859-1",quotechar='"').set_index("time",drop=False)
    data.index = pd.to_datetime(data.index)
    return data.loc[data.index>(dt.now()-pd.Timedelta(seconds=window))]
# Constants
# 'config'
rolling_window = 2 # in Seconds
step_size = 1 # in Seconds
relevant_col = ["key_strokes" ,  "key_press_time" , "key_no_dead_time" , "key_dead_time_avg",  "key_deletions"]
model_type = "rf"
CONSOLE_SHOWN = subprocess.CREATE_NEW_CONSOLE if True else subprocess.CREATE_NO_WINDOW

weights= {
    "rf": "./volume/rf_weights_key.dat",
    "cnn": "woer"
}
predicton_fnc = {
    "rf":getRF,

}



# start

    # load models
model = predicton_fnc[model_type]()

    # start sensors

key_mouse = subprocess.Popen(f"{sys.executable} ./tracking/keyboard_mouse_tracker.py test test_", shell = False,creationflags = CONSOLE_SHOWN)
#import subprocesses --> like in study
stopped = False
#start
while not stopped:
    
    #get last windowsize from data
    data = get_data(window=rolling_window)
    #print(data)
    calc_data = KeyMouse(data,pd.Timedelta(seconds=rolling_window)).out_dict()
    #print(calc_data)
    calc_data_df = pd.DataFrame([calc_data]).replace(np.nan,0)
    #print(calc_data_df)
    #prediction
    if not calc_data_df.empty:
        to_convert = ["key_press_time","key_dead_time_avg"]
        for val in to_convert:
            #print(train_data)
            calc_data_df[val] = pd.to_timedelta(calc_data_df[val])/pd.Timedelta(seconds=1)
        output = model.predict(calc_data_df[relevant_col])
        # display data
        #print(calc_data[relevant_col])
        print(output)
    # sleep until next timeframe

    
    #stopped= True
psutil.Process(key_mouse.pid).kill()

