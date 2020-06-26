import pandas as pd

def case_time_series():

    df = pd.read_csv("https://api.covid19india.org/csv/latest/case_time_series.csv")
    df['Date'] = df['Date'].astype('str') + "2020"
    df['Date'] = pd.to_datetime(df['Date'],format="%d %B %Y")
    df['Date'] = df['Date'].astype('datetime64[ns]')
    return df