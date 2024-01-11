import pandas as pd 
import numpy as np
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay
import matplotlib.pyplot as plt

def matrix_gen(df):
    cm = confusion_matrix(df["target"], df["output"])
    dspl = ConfusionMatrixDisplay(confusion_matrix=cm)
    dspl.plot()
    plt.show()
    pass


df = pd.DataFrame({"output":[0,0,0,1,1,1,2,2,2], "target":[0,1,2,0,1,2,2,2,2]})
df = pd.read_csv("./test_cnn_cat_MOUSE_2.csv")
matrix_gen(df)
