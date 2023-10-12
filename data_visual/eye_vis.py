import pandas as pd
import ast

# read data 

path = "./file/e_reye_logging.log"
data = pd.read_csv(path)

left_eye = data.loc[data["location"] == "gaze_left"].set_index("time")
left_eye["event2"] =left_eye["event"].apply(lambda x: ast.literal_eval(str(x)))
right_eye = data.loc[data["location"] == "gaze_right"].set_index("time")
right_eye["event2"]=right_eye["event"].apply(lambda x: ast.literal_eval(str(x)))
print(left_eye["event2"].iloc[1][0])
print(left_eye)



