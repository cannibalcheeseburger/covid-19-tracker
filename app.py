import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import src
import plotly.express as px
import json

time_series  = src.case_time_series()
state_total,last_update = src.states_wise()
state_daily = src.daily_state()


external_stylesheets = ['https://raw.githubusercontent.com/plotly/dash-sample-apps/master/apps/dash-datashader/assets/style.css']
tickFont = {'size':12, 'color':"rgb(30,30,30)", \
            'family':"Courier New, monospace"}



app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.title =  'Covid-19 Tracker'

app._favicon = 'img/favicon.png'

app.layout = html.Div( children  = [
    html.H1(children = "Hello dash", id = 'h1id'),

    html.H3(children = "LAST UPDATED: "+str(last_update)),
    dcc.Dropdown(
        id = 'dropdown',
        options=[
             {'label': i, 'value': j} for i,j in zip(state_total.State.unique(),state_total.State_code.unique())
        ],
        value='TT'
    ),
    dcc.Graph(
        id = 'time-series-total',
            ),
    dcc.Graph(
        id = 'time-series-daily',
    ),
    dcc.Graph(
        id = 'state-wise',
        figure = px.scatter(state_total[1:],x = 'Deaths', y ='Confirmed',size_max=150,title='yyas',size='Deaths',color='State',log_x=True),        
    ),
])


@app.callback(
    [Output('time-series-total','figure'),
    Output('time-series-daily','figure')],
    [Input('dropdown','value')]
)

def update_graph(drop_value):
    
    if drop_value == 'TT':
        figure = px.line(time_series,x = 'Date', y ='Total Confirmed',title='Time Series Total')
        figure.add_scatter( x = time_series['Date'],y=time_series['Total Deceased'],name='Deceased')
        figure.add_scatter( x = time_series['Date'],y=time_series['Total Recovered'],name='Recovered')
        daily_fig = px.line(time_series,x = 'Date', y ='Daily Confirmed',title='Daily Time Series')   
        daily_fig.add_scatter( x = time_series['Date'],y=time_series['Daily Deceased'],name='Deceased')
        daily_fig.add_scatter( x = time_series['Date'],y=time_series['Daily Recovered'],name='Recovered')

    else :
       
        figure = px.line(time_series,x = 'Date', y ='Total Confirmed',title='Time Series Total')
        daily_fig = px.line(state_daily[state_daily['Status']=='Confirmed'],x = 'Date',y = drop_value,title='Daily Time Series')
        daily_fig.add_scatter(x = state_daily[state_daily['Status']=='Recovered']['Date'],y = state_daily[state_daily['Status']=='Recovered'][drop_value],name='Recovered')
        daily_fig.add_scatter(x =state_daily[state_daily['Status']=='Deceased']['Date'],y = state_daily[state_daily['Status']=='Deceased'][drop_value],name='Deceased')

    figure.update_layout(transition_duration=500)
    daily_fig.update_layout(transition_duration=500)

    return figure,daily_fig

server = app.server

if __name__ == "__main__":
    app.run_server(debug = True)
