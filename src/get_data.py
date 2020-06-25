
import pandas as pd

baseURL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
def loadData(fileName, columnName):
    data = pd.read_csv(baseURL + fileName) \
             .drop(['Lat', 'Long'], axis=1) \
             .melt(id_vars=['Province/State', 'Country/Region'], 
                 var_name='date', value_name=columnName) \
             .astype({'date':'datetime64[ns]', columnName:'Int64'}, 
                 errors='ignore')
    data['Province/State'].fillna('<all>', inplace=True)
    data[columnName].fillna(0, inplace=True)
    return data