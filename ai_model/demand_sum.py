import pandas as pd
import os

ORDER_DICT = {
    "a":[0,1,2],
    "b":[1,2,0],
    "c":[2,0,1],
    "d":[2,1,0],
    "e":[0,2,1],
    "f":[1,0,2],
}

path = "./demands/"

files = [path+file for file in os.listdir(path=path)]

data = []
for file in files:
    temp_data = pd.read_csv(file)
    name_ID = file.split("/")[-1].split("_")[0]
    temp_data["name"] = name_ID[:-1]
    print(ORDER_DICT[name_ID[-5]][int(name_ID[-1])])
    temp_data["diff"] =ORDER_DICT[name_ID[-5]][int(name_ID[-1])]
    data.append(temp_data)

data = pd.concat(data)
data.to_csv("./total_demands_new.csv")
print(data)