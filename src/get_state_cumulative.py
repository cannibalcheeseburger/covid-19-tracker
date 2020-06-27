import pandas as pd
def state_cumu():
    df = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv")
    columns = df.columns[2:]
    date = pd.to_datetime(df['Date'], format ="%d-%b-%y")
    status = df['Status']
    df = df.pivot(index='Date', columns='Status')
    df= df.cumsum(axis=0)
    df = df.stack()
    df.to_csv("./csv/state_cumu.csv",index = False)
    df = pd.read_csv("./csv/state_cumu.csv",names=columns,skiprows=1)
    df['Date']=date
    df['Status']=status
    return df