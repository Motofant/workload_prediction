import pandas as pd
import numpy as np
from enum import Enum
import os
import joblib
from constants_correl import MODE,MODELS, calc_weighted_target, get_relevant_metrics

# constants
to_convert = ["key_press_time","key_dead_time_avg"]
target_col = "goal"
all_user = [
    "probe1bcab",
    "probe2cabb",
    "stuafce",
    "stubacf",
    "studdac",
    "studfed",
    "stuebcd",
    "stuecfa",
    "stufaef",
    "stucdea",
    ]

# variables 
## paths
WEIGHTS_PATH = "./weights_30_5/"
GEN_INFO_PATH = "./processed_30_5apart/"
#DATA_PATH = "./processed_30_5apart_test/"
DATA_PATH = "./processed_30_5apart/"

training_mode = MODE.CLICK
testing_mode = MODE.DRAG

testing_user = "studdac"# all_user[9]
model = MODELS.RF_CLASS_3.value
weighted =  model["mode"] != "classification"

small_window = False



# get weights
## uses weights from 90-10 
possible_weights = [WEIGHTS_PATH+file for file in os.listdir(WEIGHTS_PATH) if (training_mode.name in file) and ("90_10" in file )and (("class" in file) == ("class" in model["mode"])) and ( (int(file.split("_")[6]) == model["classes"]) or ("class" not in model["mode"]) ) ]
  
print(possible_weights)
print(len(possible_weights))
# select file with highest acc
results = [float(".".join(x.split("/")[-1].split(".")[0].split("_")[-2:])) for x in possible_weights]
best_result = results.index(max(results)) if model["mode"] == "classification" else results.index(min(results))

# select weights of best modell
print(best_result)
weights = possible_weights[best_result] 
print(weights)

# read general info
general_info_data = pd.read_csv(GEN_INFO_PATH + "general_info.csv")
print(general_info_data)

# get and sort files
# get files for testing

file_lst = [file for file in os.listdir(DATA_PATH) if (testing_user in file) and (any(check_string in file for check_string in testing_mode.value)) ]

# get relevant metrics
cols = get_relevant_metrics(mode=training_mode.name, small_window=small_window, weighted=weighted)


output_dfs = []
for testing_data_file in file_lst:
    # get tlx value 
    demands = [DATA_PATH+file for file in os.listdir(DATA_PATH) if ("demand" in file) and (file.split("_")[0] in testing_data_file.split("/")[-1].split("_")[0])][0] 
    #print(demands)
    testing_data = pd.read_csv(DATA_PATH+testing_data_file)
    #print(model)
    if model["mode"] == "regression":
        value = calc_weighted_target(data_file=testing_data_file, target=pd.read_csv(demands).to_dict(orient="records")[0])
        #print(value)
        testing_data[target_col] = value 
    else:
        name = demands.split("/")[-1].split("_")[0]
        print(name)
        value = general_info_data.loc[general_info_data["name"]== name, "difficulty"].values.tolist()[0]

        testing_data[target_col] = value 
        
        # modify classification when only two tasks are used 
        if model["classes"] == 2:
            if value == 1 and testing_mode.name != "WRITE": 
                print("skipped ")
                continue 
            if value == 2:
                testing_data[target_col] = 1 

    
    for val in to_convert:
        testing_data[val] = pd.to_timedelta(testing_data[val])/pd.Timedelta(seconds=1)
    testing_data = testing_data.replace(np.NaN,0)

    #print(weights )


    # read model with weights
    prediction_model = joblib.load(weights)

    # predict data
    prediction =prediction_model.predict(testing_data[cols])

    # show results

    print(general_info_data.loc[general_info_data["name"] == demands.split("/")[-1].split("_")[0], "difficulty"].values.tolist()[0])
    x = pd.DataFrame({"output":prediction,  "target":testing_data[target_col], "diff":abs(prediction-testing_data[target_col])})    

    if model["mode"]== "regression":
        
        print(str(x["diff"].mean()).replace(".",","))
        print(str(x["diff"].min()).replace(".",","))
        print(str(x["diff"].max()).replace(".",","))
        print(str(x["diff"].std()).replace(".",","))
    else:
        false_occ = x["diff"].astype(bool).sum(axis=0)
        print(str((x.shape[0]-false_occ)/x.shape[0]).replace(".",","))
        print()
        #print(x)

    output_dfs.append(x)

if len(output_dfs)==1:
    x = output_dfs[0]
else:
    x = pd.concat(output_dfs)
false_occ = x["diff"].astype(bool).sum(axis=0)
if model["mode"]== "regression":
    print(x)
    print(str(x["diff"].mean()).replace(".",","))
    print(str(x["diff"].min()).replace(".",","))
    print(str(x["diff"].max()).replace(".",","))
    print(str(x["diff"].std()).replace(".",","))
#print(x)
else:
    false_occ = x["diff"].astype(bool).sum(axis=0)
    print(x)
    oi = pd.Categorical(x["output"],categories=[0,1,2]).value_counts()
    print(oi[0])
    print(oi[1])
    print(oi[2])
    #print(x["output"].groupby(1).count())
    print(str((x.shape[0]-false_occ)/x.shape[0]).replace(".",","))
    
# save outputs
temp = "classes"
temp_2 = "classification"
output_file_ID = f"change_tasks_{model['mode']}{f'_{model[temp]}'if model['mode'] == temp_2 else ''}_{training_mode.name}_{testing_mode.name}_{testing_user}"
x.to_csv(f"./prognose_test/{output_file_ID}.csv", index = False)