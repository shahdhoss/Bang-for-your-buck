import numpy as np
import pandas as pd

def preprocessing(file):
    df = pd.read_csv(file)
    x=df.iloc[:,2:4]
    y=df.iloc[:,4]
    return x,y