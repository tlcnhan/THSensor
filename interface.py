import pandas as pd
import time
import matplotlib.pyplot as plt



while True:
    df = pd.read_csv("temp-humid.csv")
    df["temperature"] = pd.to_numeric(df["temperature"], errors = "ignore")
    df["humidity"] = pd.to_numeric(df["humidity"], errors = "ignore")
    
    #fig, ax = plt.subplots()
    df.set_index("time")
    end = df.index.max()
    start = end -10
    df= df.loc[start:end]
    #print(df.tail())
    plt.pause(0.01)
    
    ax = plt.gca()
    df.plot(kind='line',x = 'time', y='temperature', ax=ax)
    df.plot(kind='line',x='time',y='humidity', color='red', ax=ax)
    plt.show()
    time.sleep(2)