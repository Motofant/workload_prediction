import pandas as pd
import ast
import json
import numpy as np
class EyeTrack:
    sensor_type = "perif"
    dimension = "location"
    value = "event"

    def __init__(self, data) -> None:
        # get Data
        data.index = pd.to_datetime(data.index)
        self.pupil_size_data = data.loc[data[self.dimension] == "pupil_diameter"]
        self.pupil_size_data[self.value] = self.pupil_size_data[self.value].str[1:-1]
        self.pupil_size_data["left"] = [float(tup[0]) for tup in self.pupil_size_data[self.value].str.split(",")]
        self.pupil_size_data["right"] = [float(tup[1]) for tup in self.pupil_size_data[self.value].str.split(",")]
        if len(self.pupil_size_data):
            self.pupil_size_calc()
        else:
            self.avg_size_left, self.max_size_left ,self.min_size_left =0
        
        self.gaze_right = data.loc[data[self.dimension] == "gaze_right"]
        self.gaze_right[self.value] = self.gaze_right[self.value].str[1:-1]
        self.gaze_right["x"] = [float(tup[0]) for tup in self.gaze_right[self.value].str.split(",")]
        self.gaze_right["y"] = [float(tup[1]) for tup in self.gaze_right[self.value].str.split(",")]

        #self.avg_distance_right, self.avg_speed_right = self.get_eye_movements(self.gaze_right)


        self.gaze_left = data.loc[data[self.dimension] == "gaze_left"]
        self.gaze_left[self.value] = self.gaze_left[self.value].str[1:-1]
        self.gaze_left["x"] = [float(tup[0]) for tup in self.gaze_left[self.value].str.split(",")]
        self.gaze_left["y"] = [float(tup[1]) for tup in self.gaze_left[self.value].str.split(",")]
        #self.avg_distance_left, self.avg_speed_left = self.get_eye_movements(self.gaze_left)

    def get_eye_movements(self,data):
        eye_remove_doup = data[~data.index.duplicated(keep = "first")]
        #eye_remove_doup['x'] = [int(tup[0][1:]) for tup in eye_remove_doup['event'].str.split(",")]
        #eye_remove_doup['y'] = [int(tup[1][:-1]) for tup in eye_remove_doup['event'].str.split(",")]

        # calc distance between rows via pythagoras 
        # TODO: split mouse movemnt in swipes (some deadtime between moevments)
        #for n,col in enumerate(["x","y"]):
            #mouse_remove_doup[col] = #mouse_remove_doup['event'].apply(lambda location: int(location[n]))
        eye_remove_doup["xdiffsq"] = eye_remove_doup["x"].diff().pow(2)
        eye_remove_doup["ydiffsq"] = eye_remove_doup["y"].diff().pow(2)
        eye_remove_doup["timediff"] = eye_remove_doup.index.to_series().diff().div(np.timedelta64(1, 's'))
        eye_remove_doup["distance"] = np.sqrt(eye_remove_doup["xdiffsq"]+eye_remove_doup["ydiffsq"])
        eye_remove_doup["velocity"] = eye_remove_doup["distance"].div(eye_remove_doup["timediff"]) 
        output = eye_remove_doup 
        return output["distance"].mean(),output["velocity"].mean()  

    def pupil_size_calc(self):
        self.avg_size_left = self.pupil_size_data["left"].mean()
        self.max_size_left = self.pupil_size_data["left"].max()
        self.min_size_left = self.pupil_size_data["left"].min()
        self.nan_pup_left = self.pupil_size_data["left"].isna().sum() 

        self.avg_size_right = self.pupil_size_data["right"].mean()
        self.max_size_right = self.pupil_size_data["right"].max()
        self.min_size_right = self.pupil_size_data["right"].min()
        self.nan_pup_right = self.pupil_size_data["right"].isna().sum() 

    def output_dict(self):
        return{
            "avg_size_left":self.avg_size_left,
            "max_size_left":self.max_size_left, 
            "min_size_left":self.min_size_left,
            "nan_pup_left":int(self.nan_pup_left),

            "avg_size_right":self.avg_size_right, 
            "max_size_right":self.max_size_right,
            "min_size_right":self.min_size_right,
            "nan_pup_right":int(self.nan_pup_right),
            #"avg_distance_right":self.avg_distance_right, 
            #"avg_speed_right":self.avg_speed_right,
            #"avg_distance_left":self.avg_distance_left, 
            #"avg_speed_left":self.avg_speed_left,

        }
if __name__ == '__main__':
    data = pd.read_csv("./data_processing/logging/Sensor_test_1_dragging_eye_logging.log", encoding="ISO-8859-1",quotechar='"',dtype={"perif":str, "location":str, "value":object}).set_index("time",drop=False)
    x = EyeTrack(data=data)
    print(x.output_dict())

    print(json.dumps(x.output_dict(), indent=2))