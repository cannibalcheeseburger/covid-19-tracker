import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import src
import plotly.express as px


time_series  = src.case_time_series()
state_total,last_update = src.states_wise()




external_stylesheets = ['https://github.com/plotly/dash-app-stylesheets/blob/master/dash-diamonds-explorer.css']
tickFont = {'size':12, 'color':"rgb(30,30,30)", \
            'family':"Courier New, monospace"}

time_fig = px.line(time_series,x = 'Date', y ='Total Confirmed',title='Time Series Total')
time_fig.add_scatter( x = time_series['Date'],y=time_series['Total Deceased'],name='Deceased')
time_fig.add_scatter( x = time_series['Date'],y=time_series['Total Recovered'],name='Recovered')

daily_fig = px.line(time_series,x = 'Date', y ='Daily Confirmed',title='Time Series Daily')   
daily_fig.add_scatter( x = time_series['Date'],y=time_series['Daily Deceased'],name='Deceased')
daily_fig.add_scatter( x = time_series['Date'],y=time_series['Daily Recovered'],name='Recovered')

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div( children  = [
    html.H1(children = "Hello dash", id = 'h1id'),

    html.H3(children = "LAST UPDATED: "+str(last_update)),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),
    dcc.Graph(
        id = 'time-series-total',
        figure = time_fig,        
    ),
    dcc.Graph(
        id = 'time-series-daily',
        figure = daily_fig,
    ),
    dcc.Graph(
        id = 'state-wise',
        figure = px.scatter(state_total,x = 'Deaths', y ='Confirmed',title='yyas',size='Deaths',color='State',log_x=True,log_y=True),        
    ),
])



if __name__ == "__main__":
    app.run_server(debug = True)
