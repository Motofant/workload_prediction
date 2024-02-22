import pandas as pd
import numpy as np
import keras
from keras.models import Sequential
from keras.utils import to_categorical
from keras.layers import MaxPool1D, Dense, Conv1D, LSTM,MaxPooling1D,Dropout, Flatten
import os
from enum import Enum
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.preprocessing import PolynomialFeatures,OneHotEncoder
import joblib
from xgboost import XGBClassifier
from constants_correl import MODE, get_relevant_metrics,calc_weighted_target

# constants
target_col = "goal" # name of column containing target value
single_target_col = "_mental" 
to_convert = ["key_press_time","key_dead_time_avg"]
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

sample_len = 10 # samples for cnn
    

# functions
def calc_weighted_target_old(data_file, user_name, target):
    user_name = data_file.split(".")[0].split("_")[0][:-1]
    task_type = data_file.split(".")[0].split("_")[1]

    user_data_path = "./nutzerdaten.xlsx"
    user_data = pd.read_excel(user_data_path)
    user_data = user_data.loc[user_data["ID"] == user_name]
    print("________")
    print(data_file)
    print(target)
    print(user_data)
    
    workloads = []
    for key in target.keys():
        if task_type in key:
            print(task_type, key)
            print(target[key], user_data[key.split("_")[1]].values.tolist()[0])
        
            workloads.append(target[key] * user_data[key.split("_")[1]].values.tolist()[0])
    print(sum(workloads))
    print(sum(workloads)/3)
    return sum(workloads)/3

def createModel(sample_len,n_features):
    #print(sample_len, n_features)
    model = Sequential()
    model.add(Conv1D(filters=512, kernel_size=5, activation='relu', input_shape=(sample_len, n_features)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(.3))
    model.add(Conv1D(filters=512, kernel_size=2, activation='relu',))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(.3))
    model.add(Dense(1))

    optimizer = keras.optimizers.Adam(learning_rate=0.00001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy',metrics= ['accuracy'],experimental_run_tf_function=False)
    #print(model.summary())
    return model

def createModelCat_current(sample_len,n_features):
    #print(sample_len, n_features)
    model = Sequential()
    model.add(Conv1D(filters=1024, kernel_size=5, activation='relu', input_shape=(sample_len, n_features)))
    #model.add(Conv1D(filters=1024, kernel_size=4, activation='relu', input_shape=(sample_len, n_features)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dense(2048, activation='relu'))
    model.add(Flatten())
    model.add(keras.layers.BatchNormalization())
    #model.add(Dropout(.3))
    model.add(Dense(3,activation="softmax"))

    optimizer = keras.optimizers.Adam(learning_rate=0.00001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy',metrics= ['accuracy'],experimental_run_tf_function=False)
    #print(model.summary())
    return model

def createModelCat(sample_len,output):
    #print(sample_len, n_features)

    model = Sequential()
    #model.add(Conv1D(filters=124, kernel_size=5, activation='relu', input_shape=(sample_len, n_features)))
    
    model.add(Dense(1024,input_shape = (sample_len[0],),activation="relu"))
    model.add(keras.layers.BatchNormalization())
    model.add(Dense(2048,activation="relu"))
    model.add(Dense(2048,activation="relu"))
    model.add(keras.layers.BatchNormalization())
    model.add(Dense(1024,activation="relu"))
    model.add(Dense(1024,activation="relu"))
    model.add(keras.layers.BatchNormalization())
    model.add(Dense(512,activation="relu"))
    model.add(Dense(512,activation="relu"))    
    model.add(keras.layers.BatchNormalization())

    model.add(Dense(output,activation="softmax"))

    optimizer = keras.optimizers.Adam(learning_rate=0.00001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy',metrics= ['accuracy'],experimental_run_tf_function=False)
    return model

def createModel_odl(input_dim, output_dim):
    # https://stats.stackexchange.com/questions/305863/how-to-train-lstm-model-on-multiple-time-series-data
    x = 2
    y = 2
    z = 512
    model = Sequential()
    #model.add(keras.Input(shape=(input_dim,)))
    #model.add(keras.layers.LSTM(30,input_shape=(1,input_dim,)))
    model.add(Dense(z,input_shape = (input_dim,), activation='relu'))

    model.add(Dense(z, activation='relu',))
    model.add(Dropout(.2))
    model.add(keras.layers.BatchNormalization())
    
    model.add(Dense(z, activation='relu',))
    model.add(Dropout(.2))
    model.add(Dense(z, activation='relu',))
    model.add(Dense(z, activation='relu',))
    #model.add(keras.layers.BatchNormalization())

    #model.add(keras.layers.BatchNormalization())
    #model.add(Dense(10, activation='sigmoid'))

    #model.add(keras.layers.BatchNormalization())
    #model.add(Dense(10, activation='sigmoid'))
    #model.add(Dropout(.5))
    #model.add(keras.layers.Flatten())

    model.add(Dense(output_dim, activation="relu"))
    
    optimizer = keras.optimizers.Adam(lr=.000001)
    model.compile(loss='mae', optimizer=optimizer, metrics= ['mean_squared_error', 'mean_absolute_error','accuracy'],experimental_run_tf_function=False)

    return model

def createModel_cnn(input_dim, output):
    model = Sequential()

    model.add(Conv1D(1024,20,input_shape=input_dim,activation="softmax",padding="same"))
    model.add(MaxPooling1D(2,data_format="channels_first"))     
    model.add(Dense(2048, activation='softmax'))
    
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Flatten())
    model.add(Dense(output,activation="relu"))

    optimizer = keras.optimizers.Adam(lr=0.00005)
    model.compile(loss='mse', optimizer=optimizer, metrics=['mean_squared_error', 'mean_absolute_error','accuracy'],experimental_run_tf_function=False)
    return model

def createModel_final_cat(input_dim,output):
    model = Sequential()
    model.add(Dense(64, input_shape=input_dim, activation="softmax"))
    model.add(Dense(64,activation="relu"))
    model.add(Dense(64,activation="relu"))
    model.add(Dense(output,activation="relu"))

    optimizer = keras.optimizers.Adam(learning_rate=0.00001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy',metrics= ['accuracy'],experimental_run_tf_function=False)
    return model

if __name__ == "__main__":
    # Configuration
    ## Prediction System
    ### In use
    random_forest = True
    random_forest_class = False
    
    ### not currently working
    svm_prediction = False
    ploy_regr = False # not working
    cnn = False
    cnn_cat = False
    fin_dense = False
    xgboost = False
    svm_prediction_class = False
    
    ### Part of total data used 
    mode = MODE.PHRASE

    ## Target Value
    weighted = True # Use NASA-TLX as traget --> used in regression
    workload_level = False # Use workload level --> used in classification

    ### Use only max and min value as targetdata only works with workload_level
    two = False 

    ## Data Configuration
    ### use one User as prediction data otherwise use 10% of data per user for prediction
    new_user = False # Use single user as predictiondata 
    test_user = all_user[0] # Selected Testuser --> only used if 
    

    ### Import path
    # contains all files 
    FILE_PATH = "./processed_30_5apart/"
    #FILE_PATH = "./processed_2_1apart/"

    small_window = "2_1" in FILE_PATH
    
    ## get general info
    general_info_data = pd.read_csv(FILE_PATH + "general_info.csv")

    ## sort files by name 
    files = [f for f in os.listdir(FILE_PATH)]
    
    sorted_files = {} # contains data files, key -> username+iteration, value list
    label = {} # contains files of TLX-Results 
    
    # filter files
    for f in files:
        split_str = f.split("_") 
        if "demand" in split_str[1]:
            label[split_str[0]] = f

        elif split_str[0] not in sorted_files.keys():
            if any(task in f for task in mode.value):
                sorted_files[split_str[0]] = [f]
        else:
            if any(task in f for task in mode.value):
                sorted_files[split_str[0]].append(f)


    # read data files, add target column
    train_data = pd.DataFrame()
    test_data = pd.DataFrame()

    for key,lst in sorted_files.items():
        ## read TLX-data
        target = pd.read_csv(FILE_PATH+label[key]).to_dict(orient="records")[0] 

        for i in lst:
            ## read data files
            read_data = pd.read_csv(FILE_PATH+i).fillna(0)
            read_data = read_data.replace("NaN",0)
            read_data["name"] = key
            
            ## convert timedeltas to seconds when necessary
            for val in to_convert:
                read_data[val] = pd.to_timedelta(read_data[val])/pd.Timedelta(seconds=1)
            
            # add target column
            if weighted:
                x = calc_weighted_target(data_file = i, target = target)
                read_data.loc[:, target_col] = x
            elif workload_level:
                read_data = read_data.drop(columns=["time"])
                read_data[target_col] = general_info_data.loc[general_info_data["name"] == key, "difficulty"].values.tolist()[0]
                print(read_data.head())
            else:
                read_data[target_col] = target[i.split(".")[0].split("_")[1] + "_mental"]* 5
            ## data splitting 
            ### splitting data in train- and test-data  
            if new_user:
                ### data is divided by username
                if test_user in key:
                    if test_data.shape[0] != 0:
                        test_data = pd.concat([test_data,read_data]).fillna(0)
                    else:
                        test_data = read_data 
                else:
                    print("training "+key)
                    if train_data.shape[0] != 0:
                        train_data = pd.concat([train_data, read_data]).fillna(0)
                    else:
                        train_data = read_data
            else:
                # data is divided in 85% train rest testdata 
                idx = read_data.sample(frac = .9).index.to_list()
                if train_data.shape[0] != 0:

                    train_data = pd.concat([train_data, read_data.loc[read_data.index.isin(idx)]]).fillna(0)
                    test_data = pd.concat([test_data,read_data.loc[read_data.index.isin(idx) == False]]).fillna(0)

                    #print(train_data.head())
                else:
                    train_data = read_data.loc[read_data.index.isin(idx)]
                    test_data = read_data.loc[read_data.index.isin(idx) == False]   

        
    # removes middle category if wanted
    if two and not weighted:
        train_data = train_data.loc[train_data["goal"] != 1]
        test_data = test_data.loc[test_data["goal"] != 1]
        train_data["goal"] = train_data["goal"].map(lambda val : 1 if val == 2 else val)
        test_data["goal"] = test_data["goal"].map(lambda val : 1 if val == 2 else val)
    #print(train_data)
    print(train_data.shape, test_data.shape)
    
    cols = get_relevant_metrics(mode = mode.name, small_window=small_window, weighted=weighted)

    #print(train_data.head())
    X_lst = train_data[cols].values.tolist()
    y_lst = train_data[target_col].values.tolist()

    X_test_lst = test_data[cols].values.tolist()
    y_test_lst = test_data[target_col].values.tolist()
    #print(y_lst)

    def split_sequences(x_lst,y_lst, n_steps):
        X, y = list(), list()
        for i in range(len(x_lst)):

            # find the end of this pattern
            end_ix = i + n_steps

            # check if we are beyond the dataset
            if end_ix > len(x_lst):
                break
                # gather input and output parts of the pattern
            seq_x, seq_y = x_lst[i:end_ix], y_lst[i]
            X.append(seq_x)
            y.append(seq_y)
        return np.array(X), np.array(y)
    
    def split_sequences_transform(data,cols,target_col, n_steps):
        X, y = list(), list()
        #print(data.columns)

        for name in data["name"].unique().tolist():
            for level in data[target_col].unique().tolist():
                x_lst = data.loc[(data[target_col] == level) &( data["name"] == name),cols].values.tolist()
                y_lst = data.loc[(data[target_col] == level) & (data["name"] == name),target_col].values.tolist()
                #print(x_lst.shape)
                #print(x_lst.head())
                
                for i in range(len(x_lst)):
                    
                    # find the end of this pattern
                    end_ix = i + n_steps

                    # check if we are beyond the dataset
                    extension = []
                    if i >= len(x_lst):
                        break
                    if end_ix > len(x_lst):
                        extension = [[np.nan]*len(cols)]*(end_ix-len(x_lst))
                        #print(extension)
                        # gather input and output parts of the pattern
                    seq_x, seq_y = x_lst[i:min(end_ix,len(x_lst))]+extension,y_lst[i]
                    #print(seq_y)
                    X.append(seq_x)
                    y.append(seq_y)
        #print(len(X))
        #print(len(y))

        return np.array(X), np.array(y)

    a,b=split_sequences_transform(train_data,cols=cols,target_col=target_col,n_steps=3)
    #print(a[:4])
    #print(b[:4])

    # sampling

    #exit(1)
    n_features = len(cols)
    #print(train_data)
    #random forest
    print(test_user)    

    i = 0
    iter_max = 1 # generate multiple 
    if random_forest:
        # build random forest based on TLX results
        while i <iter_max:
            rf = RandomForestRegressor(n_estimators = 100)
            train_data = train_data.sample(frac=1)
            
            
            rf.fit(train_data[cols], train_data[target_col])
            prediction = rf.predict(test_data[cols])
            # define outputs to files 
            x = pd.DataFrame({"output":prediction,  "target":test_data[target_col], "diff":abs(prediction-test_data[target_col])})
            false_occ = x["diff"].astype(bool).sum(axis=0)
            output_file_ID = f"test_random_{mode.name}_{'2_1'if small_window else '30_5'}_{test_user if new_user else '90_10'}_{i}_{str(x['diff'].mean()).replace('.','_')}"

            x.to_csv(f"./validation/{output_file_ID}.csv", index = False)
            joblib.dump(rf,f"./weights/{output_file_ID}.dat")

            # define outputs to console
            
            if workload_level:
                print(str(x["diff"].mean()), "wrongly categorised",false_occ,"/",x.shape[0], (x.shape[0]-false_occ)/x.shape[0],"%")
            if weighted:
                print(str(x["diff"].mean()).replace(".",","))
            i+=1
    
    if random_forest_class:
        # build random forest based on workload level
        while i < iter_max:
            # prepare data 
            train_data = train_data.sample(frac= 1)
            
            # prepare weights (not used because of little shown improvements)
            sample_weights = np.ones(len(train_data[target_col]))
            class_weights = {0:1,1:1,2:1}
            if not two:
                class_weights = {0:1,1:1,2:1}
                #sample_weights[train_data[target_col]==0] = 1000000000000
                #sample_weights[train_data[target_col]==1] = 10000
                #sample_weights[train_data[target_col]==2] = .000000000001
            if two and True:
                #sample_weights[train_data[target_col]==0] = .0001
                #sample_weights[train_data[target_col]==1] = 1000
                class_weights = {0:1,1:1}
            
            # define and train classifier
            rfc = RandomForestClassifier(n_estimators=100,class_weight=class_weights)
            rfc.fit(train_data[cols], train_data[target_col], sample_weight=sample_weights)
            prediction = rfc.predict(test_data[cols])

            # save data and weights 
            x = pd.DataFrame({"output":prediction,  "target":test_data[target_col], "diff":abs(prediction-test_data[target_col])})
            false_occ = x["diff"].astype(bool).sum(axis=0)
            output_file_ID = f"test_random_class_{mode.name}_{'2_1'if small_window else '30_5'}_{2 if two else 3}_{test_user if new_user else '90_10'}_{i}_{str((x.shape[0]-false_occ)/x.shape[0]).replace('.','_')}"

            x.to_csv(f"./validation/{output_file_ID}.csv", index = False)
            joblib.dump(rfc,f"./weights/{output_file_ID}.dat")

            
            
            if workload_level:
                print(str(x["diff"].mean()), "wrongly categorised",false_occ,"/",x.shape[0], str((x.shape[0]-false_occ)/x.shape[0]).replace(".",","),"%")
                print(str((x.shape[0]-false_occ)/x.shape[0]).replace(".",","))
            if weighted:
                print(str(x["diff"].mean()).replace(".",","))
            i+=1


    ## Unoptimized trys not used in study
            
    if xgboost:
        while i < iter_max: 
            

            train_data = train_data.sample(frac= 1)
            if two:
                class_weights = {0:1,1:1}
                sample_weights = np.zeros(len(train_data[target_col]))
                sample_weights[train_data[target_col]==0] = .5
                sample_weights[train_data[target_col]==1] = 3.6

            xgb = XGBClassifier(n_estimators=1000,class_weight = class_weights)
            xgb.fit(train_data[cols], train_data[target_col])#,sample_weight=sample_weights)
            
            prediction = xgb.predict(test_data[cols])
            x = pd.DataFrame({"output":prediction.round(),  "target":test_data[target_col], "diff":abs(prediction.round()-test_data[target_col])})
            print(f"./test_xgb_class_{mode.name}_{2 if two else 3}_{test_user if new_user else '90_10'}.csv")
            x.to_csv(f"./test_xgb_class_{mode.name}_{2 if two else 3}_{test_user if new_user else '90_10'}.csv", index = False)
            false_occ = x["diff"].astype(bool).sum(axis=0)
            if workload_level:
                print(str(x["diff"].mean()), "wrongly categorised",false_occ,"/",x.shape[0], (x.shape[0]-false_occ)/x.shape[0],"%")
            if weighted:
                print(str(x["diff"].mean()))
            
            i+=1
    # svm 
    kernel = "rbf"
    #kernel = "linear"
    #kernel = "poly"
    #kernel = "sigmoid"
    
    if svm_prediction:
        i = 0
        while i <iter_max:
            svr = svm.SVR(kernel=kernel, C=1000, gamma=0.1, epsilon=0.1)
            #svr_lin = svm.SVR(kernel="linear", C=1000, gamma="auto")
            svr_ploy = svm.SVR(kernel="poly", C=1000, gamma="auto", degree=3, epsilon=0.1, coef0=1)
            
            svr.fit(train_data[cols], train_data[target_col])
            pred = svr.predict(test_data[cols])
            output = pd.DataFrame({"output":pred, "target":test_data[target_col], "diff":abs(pred-test_data[target_col])})
            print(output["diff"].mean())
            output.to_csv("./test_svm.csv", header = None, index = False)
            i+=1

    if svm_prediction_class:
        i = 0
        while i <iter_max:
            print("kujdsfahkljdsfkljhsdlkjhdfkljhsdfhkjlsdfgkhljsdf")
            svc = svm.SVC(kernel=kernel,degree=3,cache_size=1000,class_weight='balanced',C=.0005)
            #svr_lin = svm.SVR(kernel="linear", C=1000, gamma="auto")
            #svr_poly = svm.SVR(kernel="poly", C=1000, gamma="auto", degree=3, epsilon=0.1, coef0=1)
            
            svc.fit(train_data[cols], train_data[target_col])
            prediction = svc.predict(test_data[cols])

            x = pd.DataFrame({"output":prediction.round(),  "target":test_data[target_col], "diff":abs(prediction.round()-test_data[target_col])})
            print(f"./test_svm_class_{mode.name}_{2 if two else 3}_{test_user if new_user else '90_10'}.csv")
            x.to_csv(f"./test_svm_class_{mode.name}_{2 if two else 3}_{test_user if new_user else '90_10'}.csv", index = False)
            false_occ = x["diff"].astype(bool).sum(axis=0)
            if workload_level:
                print(str(x["diff"].mean()), "wrongly categorised",false_occ,"/",x.shape[0], (x.shape[0]-false_occ)/x.shape[0],"%")
            if weighted:
                print(str(x["diff"].mean()))
            i+=1

    if ploy_regr:
        i = 0
        while i < iter_max:
            # get data
            poly = PolynomialFeatures(degree=2, include_bias=False)
            poly_features = poly.fit_transform(train_data[cols])

            # define model
            model = LinearRegression()
            model.fit(poly_features,train_data[target_col])
            prediction = model.predict(test_data[cols])
            x = pd.DataFrame({"output":prediction,  "target":test_data[target_col], "diff":abs(prediction-test_data[target_col])})
            x.to_csv("./test_poly_reg.csv", header = None, index = False)
            print(x["diff"].mean())
            i+=1

    
    # sampling for neural networks
    X, y = split_sequences(X_lst,y_lst, sample_len)
    X_test,y_test = split_sequences(X_test_lst,y_test_lst, sample_len)
    #cols = cols+[target_col]
    X, y = split_sequences_transform(train_data,cols=cols,target_col=target_col,n_steps=sample_len)
    X_test,y_test= split_sequences_transform(test_data,cols=cols,target_col=target_col,n_steps=sample_len)

    

    if cnn:
        i = 0
        while i <iter_max:
            # define model
            #model = createModel(sample_len=sample_len, n_features=n_features)
            model = createModel_cnn(input_dim=(sample_len,n_features), output_dim=n_features)
            # fit model
            model.fit(X, y, epochs=50, shuffle=True,verbose=True)
            yhat = model.predict(X_test, verbose=0)
            data = []
            for nr, row in enumerate(yhat):
                data.append(row[0])
                #print(row , y_test[nr])
            x = pd.DataFrame({"output":data,  "target": y_test, "diff":abs(data-y_test)})
            x.to_csv("./test_cnn.csv", header = None, index = False)
            print(x["diff"].mean())
            i+=1

    if cnn_cat:

        i = 0

        # one hot encoding 
        ohe = OneHotEncoder()
        #y = train_data[target_col]
        #print(y.reshape(-1,1))
        #y = ohe.fit_transform(y.reshape(-1,1))
        
        #y_test = ohe.fit_transform(y_test.reshape(-1,1))
        y = to_categorical(y)
        #y_test = to_categorical(y_test)
        #print(X)
        #print(ohe.categories_)
        #print(y)
        #print(y_test)
        while i <iter_max:
            print(test_data.shape)
            print(y_test.shape)
            print(y_test)
            print(len(y))
            print(test_data["goal"].to_list())
            print(len(test_data["goal"].to_list()))

            #exit(1)
            # define model
            #model = createModelCat(sample_len=(sample_len,len(cols),), n_features=n_features)
            model = createModelCat(sample_len=(len(cols),),output=2 if two else 3)
            # fit model
            #model.fit(X, y, epochs=10, shuffle=True,verbose=True)
            #yhat = model.predict(X_test, verbose=0)
            print(X.shape, sample_len)
            print(train_data[cols].shape)
            print(test_data[cols].shape)
            print(model.summary())
            weights = {0:1,1:1}
            #model.fit(X,y)#train_data[target_col])
            model.fit(train_data[cols], to_categorical(train_data[target_col]), shuffle =True,epochs = 30,batch_size=200,class_weight = weights)
            yhat = model.predict(test_data[cols], verbose=0)
            data = []
            for nr, row in enumerate(yhat):
                #print(row)
                data.append(np.argmax(row))
                #print(np.argmax(row))
                #print(row , y_test[nr])

            x = pd.DataFrame({"output":data,  "target": y_test,"diff":abs(data-y_test)})
            print(f"./test_cnn_cat_{mode.name}_{2 if two else 3}_{test_user if new_user else '90_10'}.csv")
            x.to_csv(f"./test_cnn_cat_{mode.name}_{2 if two else 3}_{test_user if new_user else '90_10'}.csv", index = False)
            print(x.loc[x["output"] != x["target"]].shape[0]/len(yhat))
            print("nur 0:",x.loc[x["output"] == 0].shape[0]/len(yhat))
            print("nur 1:",x.loc[x["output"] ==1].shape[0]/len(yhat))
            print("nur 2:",x.loc[x["output"] == 2].shape[0]/len(yhat))
            
            i+=1
            false_occ = x["diff"].astype(bool).sum(axis=0)
            if workload_level:
                print(str(x["diff"].mean()), "wrongly categorised",false_occ,"/",x.shape[0], abs(x.shape[0]-false_occ)/x.shape[0],"%")

    if fin_dense:
        ohe = OneHotEncoder()
        y = to_categorical(train_data[target_col])
        X = train_data[cols]
        while i <iter_max:

            print(len(y))
            print(len(X))
            print(test_data["goal"].to_list())
            print(len(test_data["goal"].to_list()))
            #exit(1)
            # define model
            model = createModel_final_cat(input_dim=(len(cols),), output=3)
            # fit model
            
            model.fit(X, y, epochs=20, shuffle=True,verbose=True)
            
            yhat = model.predict(test_data[cols], verbose=0)
            i+=1
