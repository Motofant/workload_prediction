import pandas as pd
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
        self.nr_key_strokes = len(self.keyboard_data.loc[self.keyboard_data[self.col_event] == "pressed"])
        self.key_presses = self.get_full_press()
        self.key_press_time  = pd.Series([tup[1] for tup in self.key_presses]).mean()
        self.key_dead_times = self.get_dead_times()
        self.key_no_dead_times = len(self.key_dead_times)
        self.key_dead_time_avg = pd.Series([tup[0] for tup in self.key_dead_times]).mean()
        self.key_backspaces = 33 # TODO: Is this best way to measure mistakes

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

    def get_move_px(self):
        # every 10th mouse move event to sped up code
        # source: https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=d7fd6e066d771b98bbfa566337e231e4ab8ebe21
        pass

    def output_string(self):
        # returns console output to test
        print(f'TIME:')
        print(f'Timeframe: {self.time_frame}\nEndtime: {self.max_time}\n')
        print(f'Keyboard:\nN.o. Activations: {self.nr_key_strokes}\nAvg. Presstime: {self.key_press_time}\nAvg. Deadtime: {self.key_dead_time_avg}')

class KeyPress:
    # one Keypress
    def __init__(self) -> None:
        pass
class KeyPressLetter:
    # all completed presses of one letter in timeframe
    def __init__(self) -> None:
        self.start_time = True