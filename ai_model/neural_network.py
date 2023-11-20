import pandas as pd
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import MaxPool1D, Dense, Conv1D
import os
import matplotlib.pyplot as plt
# import data 



def createModel(input_dim, output_dim):
    # https://stats.stackexchange.com/questions/305863/how-to-train-lstm-model-on-multiple-time-series-data
    model = Sequential()
    model.add(Dense(input_dim, activation='relu'))
    #model.add(Dense(500, activation='sigmoid'))
    model.add(Dense(output_dim))

    optimizer = keras.optimizers.Adam(lr=0.00001)
    model.compile(loss='msle', optimizer='adam', metrics= ['mean_squared_error', 'mean_absolute_error','accuracy'])

    return model


def visualHist(history):
    ## shows visualization of accuracy and loss of network after training is completed 
    
    # history: network parameters progress over time 
    
    # summarize history for accuracy
    plt.plot(history.history['accuracy'])

    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['dense_accuracy'], loc='lower right')
    plt.show()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['dense_loss'], loc='upper right')
    plt.show()

if __name__ == "__main__":

    # get import 
    FILE_PATH = "./test_2/"

    files = [f for f in os.listdir(FILE_PATH)]
    sorted_files = {}
    label = {}
    # sort to allow labeling
    for f in files:
        split_str = f.split("_") 
        if "demand" in split_str[1]:
            label[split_str[0]] = f
        elif split_str[0] not in sorted_files.keys():
            sorted_files[split_str[0]] = [f]
        else:
            sorted_files[split_str[0]].append(f)
    
    target_col = "goal"
    train_data = pd.DataFrame()
    test_data = pd.DataFrame()
    # startt albelling
    for key,lst in sorted_files.items():
        target = pd.read_csv(FILE_PATH+label[key]).to_dict(orient="records")[0]
        print(target)
        # get demands
        for i in lst:
            read_data = pd.read_csv(FILE_PATH+i).fillna(0)
            read_data = read_data.replace("NaN",0)
            read_data[target_col] = target[i.split(".")[0].split("_")[1] + "_mental"]/20

            # 90% trianing 10% test
            length = int(read_data.shape[0]*.9)
            if train_data.shape[0] != 0:

                train_data = pd.concat([train_data, read_data.iloc[:length]])
                test_data = pd.concat([test_data,read_data.iloc[length:]])
            else:
                train_data = read_data.iloc[:length]
                test_data = read_data.iloc[length:]               

            print(train_data.shape)

    model = createModel(train_data.shape[1], 1)
    train_data = train_data.drop('time', axis=1)
    test_data = test_data.drop('time', axis=1)
    to_convert = ["key_press_time","key_dead_time_avg"]
    for val in to_convert:
        train_data[val] = pd.to_timedelta(train_data[val])/pd.Timedelta(seconds=1)
        test_data[val] = pd.to_timedelta(test_data[val])/pd.Timedelta(seconds=1)

    train_data = train_data.loc[:, train_data.columns.isin([target_col,"time", "avg_size_left","avg_size_right"])]
    test_data = test_data.loc[:, test_data.columns.isin([target_col,"time", "avg_size_left","avg_size_right"])]
    
    train_data.to_csv("./train.csv")
    test_data.to_csv("./test.csv")

    print(test_data.head())
    #print(np.asarray(train_data[target_col],dtype=float))
    history = model.fit(train_data.loc[:, ~train_data.columns.isin([target_col, "time"])].astype("float"),y =np.asarray(train_data[target_col],dtype=float), shuffle = True,epochs=5,batch_size=1)
    
    #visualHist(history)
    #testing 
    predictions = model.predict(test_data.loc[:, ~train_data.columns.isin([target_col, "time"])])  
    out = []
    for row in predictions:
        row = list(row)
        i = max(row)
        out.append(i)
    #print(predictions)
    output = pd.DataFrame().from_dict({"calc":out, "column" : test_data["goal"]})
    pd.DataFrame(output).to_csv("./tetts.csv", header = None, index = False)
