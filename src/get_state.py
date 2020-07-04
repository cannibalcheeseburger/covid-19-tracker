
import pandas as pd
import datetime

def states_wise():
    df1 = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
    last_update = df1['Last_Updated_Time'].max() 
    df1 = df1.replace('Total','All States') 
    df2 = pd.read_csv('./csv/population.csv',index_col = 0)
    df = pd.merge(df1, df2, on='State',how='outer')
    return df , last_update