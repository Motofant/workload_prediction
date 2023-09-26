import pandas as pd
import numpy as np
# inspired by Analysis of Text Entry Performance Metrics 
class KeyMouse:
    col_perif = "perif"
    col_event = "event"
    col_loc = "location"
    # define Dataobj
    # input has to be sorted
    def __init__(self, all_data, tf_sec) -> None:
        # split data
        self.keyboard_data = all_data.loc[all_data[self.col_perif] == "keyboard"]
        #self.analog_data = all_data.loc[all_data[self.col_perif] == "analog"]
        self.mouse_data =  all_data.loc[all_data[self.col_perif] == "mouse"]
        #print(f"keyboard {len(self.keyboard_data)}")
        #print(f"mouse {len(self.mouse_data)}")
        # get generell info
        self.time_frame = tf_sec
        self.max_time = all_data.index.max()

        # calculate info
        # keyboard
        if len(self.keyboard_data)>0:
            self.nr_key_strokes = len(self.keyboard_data.loc[self.keyboard_data[self.col_event] == "pressed"])
            self.key_presses = self.get_full_press()
            self.key_press_time  = pd.Series([tup[1] for tup in self.key_presses]).mean()
            self.key_dead_times = self.get_dead_times()
            self.key_no_dead_times = len(self.key_dead_times)
            self.key_dead_time_avg = pd.Series([tup[0] for tup in self.key_dead_times]).mean()
            self.key_backspaces = self.get_deletions() # TODO: Is this best way to measure mistakes
        else:
            self.nr_key_strokes = 0
            self.key_presses = 0
            self.key_press_time = np.nan
            self.key_dead_times = np.nan
            self.key_no_dead_times = np.nan
            self.key_dead_time_avg = np.nan
            self.key_backspaces = 0 # TODO: Is this best way to measure mistakes
        # mouse
        self.avg_distance, self.avg_speed = self.get_move_px()
    def get_full_press(self):
        full_presses = []
        keys_grouped = list(self.keyboard_data.groupby(self.col_loc))
        
        for key_list in keys_grouped:
            key = key_list[0]
            key_data = key_list[1]
            if len(key_data)>1:

                #print(key)
                # remove incomplete presses 
                key_data_full_presses = key_data.loc[(key_data[self.col_event] == "released").idxmin() :(key_data[self.col_event] == "released")[::-1].idxmax() ]
                
                # remove double press event  TODO maybe add number 
                key_data_rem_duplicate = list(key_data_full_presses.loc[key_data_full_presses[self.col_event].shift() != key_data_full_presses[self.col_event]].groupby(self.col_event))
                if len(key_data_rem_duplicate) == 2: 
                    full_presses += [(key, 
                                    key_data_rem_duplicate[1][1].index[num] - key_data_rem_duplicate[0][1].index[num], 
                                    key_data_rem_duplicate[0][1].index[num], 
                                    key_data_rem_duplicate[1][1].index[num] ) for num, _ in enumerate(key_data_rem_duplicate[1][1].values)]
        return full_presses

    def get_avg_time(self):
        # not used, because its one line
        times = pd.Series([tup[1] for tup in self.key_presses]).mean()
        return times
    
    def get_dead_times(self):
        # TODO define edgecases
        # return max size if no complete presses
        # get complete timeframe
        out_col = "off_time"
        all_times = self.keyboard_data
        all_times = pd.concat([all_times.iloc[[0]], all_times, all_times.iloc[[-1]]])
        all_times[out_col] = True

        # filter the keypresses
        for on_time in self.key_presses:
            all_times.loc[(all_times.index > on_time[2]) & (all_times.index < on_time[3]), out_col] = False
        #print(all_times)

        press_edges = all_times.loc[all_times[out_col].shift() != all_times[out_col]]
        press_edges = press_edges.loc[(press_edges[out_col] == False).idxmin():(press_edges[out_col] == False)[::-1].idxmax() ] # TODO: change when edgecases defined
        #print(press_edges)
        
        dead_times=list((press_edges.iloc[2*i+1].name-press_edges.iloc[2*i].name, press_edges.iloc[2*i].name,press_edges.iloc[2*i+1].name,)  for i in range(int(len(press_edges)/2)))
        #print(all_times.loc[out_col == True])
        return dead_times
    
    def get_deletions(self):
        deletions = self.keyboard_data.loc[((self.keyboard_data["location"] == "key.backspace") | (self.keyboard_data["location"] == "key.delete")) & (self.keyboard_data["event"] == "pressed")]
        return len(deletions)
    

    def get_move_px(self):
        # get only mouse movemnts
        mouse_move = self.mouse_data.loc[self.mouse_data["location"] == "pos"]
        # every 10th mouse move event to sped up code
        # source: https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=d7fd6e066d771b98bbfa566337e231e4ab8ebe21
        mouse_move = mouse_move.iloc[::10, :]
        # remove douplicates in timestamp --> sometimes duplicates occur --> first value is taken
        # fastest method as shown here https://stackoverflow.com/questions/13035764/remove-pandas-rows-with-duplicate-indices
        mouse_remove_doup = mouse_move[~mouse_move.index.duplicated(keep = "first")]
        mouse_remove_doup['x'] = [int(tup[0][1:]) for tup in mouse_remove_doup['event'].str.split(",")]
        mouse_remove_doup['y'] = [int(tup[1][:-1]) for tup in mouse_remove_doup['event'].str.split(",")]

        # calc distance between rows via pythagoras 
        # TODO: split mouse movemnt in swipes (some deadtime between moevments)
        #for n,col in enumerate(["x","y"]):
            #mouse_remove_doup[col] = #mouse_remove_doup['event'].apply(lambda location: int(location[n]))
        mouse_remove_doup["xdiffsq"] = mouse_remove_doup["x"].diff().pow(2)
        mouse_remove_doup["ydiffsq"] = mouse_remove_doup["y"].diff().pow(2)
        mouse_remove_doup["timediff"] = mouse_remove_doup.index.to_series().diff().div(np.timedelta64(1, 's'))
        mouse_remove_doup["distance"] = np.sqrt(mouse_remove_doup["xdiffsq"]+mouse_remove_doup["ydiffsq"])
        mouse_remove_doup["velocity"] = mouse_remove_doup["distance"].div(mouse_remove_doup["timediff"]) 
        #mouse_remove_doup
        
        output = mouse_remove_doup 
        return output["distance"].mean(),output["velocity"].mean()  
    
    def output_string(self):
        # returns console output to test
        print(f'TIME:')
        print(f'Timeframe: {self.time_frame}\nEndtime: {self.max_time}\n')
        print(f'Keyboard:\nN.o. Activations: {self.nr_key_strokes}\nAvg. Presstime: {self.key_press_time}\nAvg. Deadtime: {self.key_dead_time_avg}')
    
    def out_dict(self):
        return{
            "key_strokes":self.nr_key_strokes, 
            #"key_presses":self.key_presses,
            "key_press_time":self.key_press_time,
            #"key_dead_time":self.key_dead_times,
            #"key_no_dead_time":self.key_no_dead_times,
            "key_dead_time_avg":self.key_dead_time_avg,
            "key_deletions": self.key_backspaces,
            "mouse_avg_distance":self.avg_distance, 
            "mouse_avg_speed":self.avg_speed,

        }

class KeyPress:
    # one Keypress
    def __init__(self) -> None:
        pass
class KeyPressLetter:
    # all completed presses of one letter in timeframe
    def __init__(self) -> None:
        self.start_time = True