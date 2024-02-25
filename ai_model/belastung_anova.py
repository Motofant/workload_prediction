import pandas as pd
import os
import pingouin as pg


def calc_weighted_target(task_type, user_name, target):
    #user_name = data_file.split(".")[0].split("_")[0][:-1]
    #task_type = data_file.split(".")[0].split("_")[1]
    print(user_name)
    print(user_name[:-1])
    user_data_path = "./nutzerdaten_anon.xlsx"
    user_data = pd.read_excel(user_data_path)
    user_data = user_data.loc[user_data["ID"] == user_name[:-1]]
    print(user_data)
    #print("________")
    #print(data_file)
    #print(target)
    #print(user_data)
    
    workloads = []
    for key in target.keys():
        if task_type in key:
            #print(task_type, key)
            #print(key, target[key], user_data[key.split("_")[1]].values.tolist()[0])
        
            workloads.append(target[key] * user_data[key.split("_")[1]].values.tolist()[0])
    #print(sum(workloads))
    #print(sum(workloads)/3)
    return sum(workloads)/3

# get data

demands_path = "./processed_30_5apart/"
user_data_path = "./nutzerdaten_anon.xlsx"
user_data = pd.read_excel(user_data_path)
gen_info = pd.read_csv(demands_path + "general_info.csv")

demands = [file for file in os.listdir(demands_path) if file.split("_")[1]=="demand.csv"]
print(demands)
outputs = []
for file in demands:
    name = file.split("_")[0]
    gen_info_user = gen_info.loc[gen_info["name"] == name]
    data = pd.read_csv(demands_path+file)
    data['difficulty'] = gen_info_user["difficulty"].values.tolist()[0]
    data['name'] = name[:-1]
    print(data)
    for task in ["writing","phrase", "clicking","dragging"]:
        data[f'{task}_tlx'] = calc_weighted_target(task,name,pd.read_csv(demands_path+file).to_dict(orient="records")[0])
    
    data = data[[col for col in data.columns.to_list() if 'writing' not in col]]
    outputs.append(data)

result = pd.concat(outputs)
print(result)
target_col = "difficulty"
an_dat_out = []
pair_test_out = []
for col in result.columns.to_list():#["phrase", "clicking","dragging"]:
    if col  in [target_col,"name"]:
        continue
    #col = col+"_tlx"
    print(col)
    an_dat = pg.rm_anova( data = result,dv = col, within=target_col,subject = "name",detailed = True)
    if "p-unc" in an_dat.keys():
        value =an_dat["p-unc"].values.tolist()[0]
        an_dat = pd.DataFrame({"col_name":[col], "andat":[value]})
        an_dat_out.append(an_dat)
    
        print(an_dat)
    pair_test = pg.pairwise_tests(data = result,dv = col,within = target_col,subject = "name", padjust = "bonf", effsize = "cohen")
    print(pair_test)
    pair_test["column"] =col
    pair_test_out.append(pair_test)
pd.concat(an_dat_out).to_csv(path_or_buf=f"./anova_res_demands.csv")
pd.concat(pair_test_out).to_csv(f"./pairwise_demands.csv",columns=["column","A","B","p-unc","T","dof","alternative","p-corr","p-adjust","BF10","cohen"])
