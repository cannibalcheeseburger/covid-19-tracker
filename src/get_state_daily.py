import pandas as pd 
def daily_state():

    df = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv")
    df['Date'] = pd.to_datetime(df['Date'],format="%d-%b-%y")

    return df