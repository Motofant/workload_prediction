import pandas as pd
import ast
import json
class EyeTrack:
    sensor_type = "perif"
    dimension = "location"
    value = "event"

    def __init__(self, data) -> None:
        # get Data
        self.pupil_size_data = data.loc[data[self.dimension] == "pupil_diameter"]
        self.pupil_size_data[self.value] = self.pupil_size_data[self.value].str[1:-1]
        self.pupil_size_data["left"] = [float(tup[0]) for tup in self.pupil_size_data[self.value].str.split(",")]
        self.pupil_size_data["right"] = [float(tup[1]) for tup in self.pupil_size_data[self.value].str.split(",")]
        if len(self.pupil_size_data):
            self.pupil_size_calc()
        else:
            self.avg_size_left, self.max_size_left ,self.min_size_left =0

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
        }
if __name__ == '__main__':
    data = pd.read_csv("./data_processing/logging/Sensor_test_1_dragging_eye_logging.log", encoding="ISO-8859-1",quotechar='"',dtype={"perif":str, "location":str, "value":object}).set_index("time",drop=False)
    x = EyeTrack(data=data)
    print(x.output_dict())

    print(json.dumps(x.output_dict(), indent=2))