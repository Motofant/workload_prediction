import pandas as pd
import numpy as np
class Analog:
    col_loc = "location"
    col_event = "event"
    col_time = "time"
    def __init__(self, data) -> None:
        self.input_data = data
        self.input_data[self.col_time] = pd.to_datetime(self.input_data[self.col_time])
        self.grouped_data = self.input_data.groupby(self.col_loc)
        self.key_actions, self.key_avgs = self.total_key_action()
        self.total_actions = [x for v in self.key_actions.values() for x in v]
        # output data
        if self.total_actions :
            total_press_time = sum([el.press_time for el in self.total_actions])
            total_release_time = sum([el.release_time for el in self.total_actions])
            self.avg_max_travel = sum([el.max_distance for el in self.total_actions])/len(self.total_actions)
            self.avg_total_time = sum([el.total_time for el in self.total_actions])/len(self.total_actions)
            self.avg_press_time = sum([el.press_time for el in self.total_actions])/len(self.total_actions)
            self.avg_press_vel =  sum([el.press_vel*el.press_time for el in self.total_actions])/total_press_time if total_press_time else 0
            self.avg_hold_time = sum([el.hold_time for el in self.total_actions])/len(self.total_actions)
            self.avg_release_time = sum([el.release_time for el in self.total_actions])/len(self.total_actions)
            self.avg_release_vel = sum([el.release_vel*el.release_time for el in self.total_actions])/total_release_time if total_release_time else 0

        else:
            self.avg_max_travel = 0
            self.avg_total_time = 0
            self.avg_press_time = 0
            self.avg_press_vel =  0
            self.avg_hold_time = 0
            self.avg_release_time = 0
            self.avg_release_vel = 0
           

    def max_distance(self):
        print(self.grouped_data.max()[self.col_event].to_dict())

    def total_key_action(self):
        # groups keydata in actions --> get split into decrease hold in increase
        # until zero
        key_presses ={}
        key_calc = {}
        for key,val in self.grouped_data:
            start_time = pd.to_datetime(val.iloc[0][self.col_time])
            press_lst = []
            for row,key_val in val.loc[val[self.col_event] == 0,:].iterrows():
                end_time = pd.to_datetime(key_val[self.col_time])
                # bulid tuple
                # get relevant data
                press_data = val.loc[(val[self.col_time]>= start_time) & (val[self.col_time] <= end_time)]
                x = KeyAction(press_data)
                press_lst.append(x)

                start_time = end_time
            key_presses[key] = press_lst
            key_calc[key] = self.avg_weighted(press_lst)
        return key_presses, key_calc
    
    def avg_weighted(self, key_data):
        key_presses = len(key_data)
        sum_total_time = sum(el.total_time for el in key_data)
        sum_press_time = sum(el.press_time for el in key_data)
        sum_hold_time = sum(el.hold_time for el in key_data)
        sum_release_time=sum(el.release_time for el in key_data)


        # output
        if sum_press_time:

            avg_vel_press = sum([el.press_vel*el.press_time for el in key_data])/sum_press_time 
            avg_vel_release = sum([el.release_vel*el.release_time for el in key_data])/sum_release_time 
        else:
            avg_vel_press = 0
            avg_vel_release = 0

        if key_presses:
            avg_time_press = sum_press_time/key_presses
            avg_time_hold = sum_hold_time/key_presses
            avg_time_release = sum_release_time/key_presses
            avg_time_total = sum_total_time/key_presses
        else:
            avg_time_press = 0
            avg_time_hold = 0
            avg_time_release = 0
            avg_time_total = 0
        
        return {
            "vel_press":avg_vel_press,
            "vel_release":avg_vel_release,
            "time_press":avg_time_press,
            "time_hold":avg_time_hold,
            "time_release":avg_time_release,
            "time_total": avg_time_total
        }

    def output_dict(self):
        return {
            "ana_max_travel":self.avg_max_travel,
            "ana_total_time":self.avg_total_time,
            "ana_press_time":self.avg_press_time,
            "ana_press_vel":self.avg_press_vel,
            "ana_hold_time":self.avg_hold_time,
            "ana_release_time":self.avg_release_time,
            "ana_release_vel":self.avg_release_vel,
        }

class KeyAction:
    col_loc = "location"
    col_event = "event"
    col_time = "time"
    def __init__(self, data:pd.DataFrame) -> None:
        self.start_press_time = data.iloc[0][self.col_time]
        self.end_press_time = data.iloc[-1][self.col_time]
        self.start_distance = data.iloc[0][self.col_event]
        self.max_distance = data[self.col_event].max()
        
        self._hold_times = data.loc[data[self.col_event] == self.max_distance]
        self.start_hold_time = self._hold_times.iloc[0][self.col_time]
        self.end_hold_time = self._hold_times.iloc[-1][self.col_time]

        # times in seconds
        self.press_time = (self.start_hold_time - self.start_press_time).microseconds / 1e6
        self.hold_time = (self.end_hold_time - self.start_hold_time).microseconds / 1e6
        self.release_time = (self.end_press_time - self.end_hold_time).microseconds / 1e6
        self.total_time = (self.end_press_time- self.start_press_time).microseconds /1e6

        self.press_vel = (self.max_distance-self.start_distance) / self.press_time if self.press_time else 0
        self.release_vel = self.max_distance / self.release_time if self.release_time else 0

        #print(self.start_distance, self.max_distance)
        #print(self.press_time, self.hold_time, self.release_time,self.total_time)
        #print(self.start_press_time, self.start_hold_time, self.end_hold_time, self.end_press_time)
        #print(self.press_vel, self.release_vel)
## Testing cases
if False:
    data = pd.DataFrame(
        {
            "time":[
                "2023-09-06 18:28:52.808376",
                "2023-09-06 18:28:52.809376",
                "2023-09-06 18:28:52.810376",
                "2023-09-06 18:28:52.811376",
                "2023-09-06 18:28:52.812377",
                "2023-09-06 18:28:52.813379",
                "2023-09-06 18:28:52.814376",
                "2023-09-06 18:28:52.815376",
                "2023-09-06 18:28:52.815377",
                ],
            "perif":["analog"]*9,
            "location":[1,1,1,1,2,2,1,2,2],
            "event":[.5,1,1,.4,.1,.8,0,.6,0],
        }
    )

    data_obj = Analog(data)
    data_obj.max_distance()
    data_obj.total_key_action()
    x = data_obj.key_avgs
    print(x)

    print("\n\n\n")
    print(f'''
        anzahl tastendrücke = {len(data_obj.total_actions)}
    avg. key travel = {data_obj.avg_max_travel}
    avg gesamtzeit: {data_obj.avg_total_time} --> press:{data_obj.avg_press_time}, hold:{data_obj.avg_hold_time}, release: {data_obj.avg_release_time}
    avg Geschwindikeiten --> press:{data_obj.avg_press_vel}, release: {data_obj.avg_release_vel}
    ''')
