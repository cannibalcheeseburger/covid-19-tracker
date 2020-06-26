
import pandas as pd
import datetime

def states_wise():
    df = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
    last_update = df['Last_Updated_Time'].max() 
    df = df.replace('Total','All')
    return df , last_update