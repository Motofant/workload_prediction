import pandas as pd

# import data ( all of it )
path = "./test.log"
window_size = pd.Timedelta(seconds=30)
window_step = pd.Timedelta(seconds=10)

fct = lambda x : print(x)
#data_analog = pd.read_csv(path_ana, delimiter= "|")
data_total = pd.read_csv(path, encoding="ISO-8859-1")

start_val =pd.to_datetime(data_total.iloc[0]["time"])
end_val =pd.to_datetime(data_total.iloc[-1]["time"])
data_total = data_total.set_index("time",drop=False)
data_total.index = pd.to_datetime(data_total.index)
data_total["time"] = pd.to_datetime(data_total["time"])

curr = start_val



# rolling window
while curr < end_val:
    # get start and end
    diff = curr + window_size

    # get data from every log
    x = data_total.loc[(data_total["time"] >= curr) & (data_total["time"] < diff)]

    curr += window_step
    print(pd.to_datetime(x.iloc[-1]["time"])-pd.to_datetime(x.iloc[0]["time"]))

## Randnotzien
# Fenstergröße --> 30 sekunden
# fensterverschiebung --> 10 sekunden nach Startzeitpunkt (nicht erster wert) --> gleichförmiges Fenster