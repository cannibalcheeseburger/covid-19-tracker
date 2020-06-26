import pandas as pd
def state_cumu():
    df = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv")
    status = df['Status']
    df['Date'] = pd.to_datetime(df['Date'], format ="%d-%b-%y")
    date = df['Date']
    df = df.pivot(index='Date', columns='Status')
    df= df.cumsum(axis=0)
    df = df.stack()
    return df