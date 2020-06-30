import pandas as pd
import os

def state_cumu():
    df = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv")
    
    df = pd.read_csv(
        "https://api.covid19india.org/csv/latest/state_wise_daily.csv")


    date = pd.to_datetime(df['Date'], format="%d-%b-%y")
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%b-%y")
    status = df['Status'].copy()

    df = df.pivot(index='Date', columns='Status')
    df = df.cumsum(axis=0)
    df = df.stack(-1)


    date = pd.DataFrame(date)
    status = pd.DataFrame(status)

    index = [x for x in range(0, len(df))]
    date_col = [date.iloc[n] for n in range(len(date))]
    status_col = [status.iloc[n] for n in range(len(status))]
    df['Index'] = index
    df = df.set_index(['Index'])

    status_col = pd.DataFrame(status_col)
    df['Status'] = status_col
    date_col = pd.DataFrame(date_col)
    df['Date'] = date_col
    return df
