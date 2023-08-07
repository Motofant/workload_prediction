import pandas as pd
import numpy as np
import datetime


roll_window_size = 3 # time based not entry based 

# define stuff
starttime = pd.Timestamp.today()
input_data = pd.DataFrame({
    "time":pd.date_range(start='2018-04-24', end='2018-04-25',periods=10).to_list(),#[starttime + datetime.timedelta(days=x) for x in range(10)],
    "perif":["key","key","key","key","key","key","key","key","key","key",],
    "key" : ["e","e","e","e","e","e","e","e","e","e",],
    "event": ["pressed","released","pressed","pressed","released","pressed","released","pressed","released","pressed",],
})



#define function stuff
def get_keystrokes (data:pd.DataFrame ):
    return len(data.loc[data["event"] == "pressed"])
    pass

def fix_data():
    # remove doubles if 
    pass

def times_calc(data:pd.DataFrame):
    # get timediff
    data["time_delta"] = (data["time"]-data["time"].shift()).fillna(0) 
    # delete oldest part until first release
    data["test"] = data["event"] == "released"
    data["test"] = data["test"].cummax()
    data_first_rel = data.loc[data["test"]]

    # get changes 
    #data_first_rel["changes"] = data_first_rel["event"].diff()
    x = data_first_rel.loc[(data_first_rel["event"] != data_first_rel["event"].shift()) &
                           (data_first_rel["event"] == "released"),"time_delta"].values.astype(np.int64)
    print(data_first_rel)
    print(x)
    x = x.mean(numeric_only=False)
    

#print(input_data)
# define output
cols = ["time_end","typing_speed"]#, "mistakes", "clicks", "doublec_interval"]
out = pd.DataFrame(columns=cols )
for window in input_data.rolling(roll_window_size, min_periods=3):
    #clean data
    
    # get values
    time_end=window["time"].iloc[-1]
    time_delta=(window["time"].iloc[-1] - window["time"].iloc[0])/ datetime.timedelta(microseconds=1)

    #print(window["time"].iloc[0])
    #print(time_end)
    typing_speed = get_keystrokes(window)/ (datetime.timedelta(days=2)/datetime.timedelta(days=1))

    out = pd.concat([out,pd.DataFrame({"time_end":[time_end],"typing_speed":[typing_speed]})])



#print(out)
print(times_calc(data=input_data))
   