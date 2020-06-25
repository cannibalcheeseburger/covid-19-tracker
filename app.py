import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import src

allData =  src.loadData("time_series_covid19_confirmed_global.csv", "CumConfirmed") \
  .merge(src.loadData("time_series_covid19_deaths_global.csv", "CumDeaths")) \
  .merge(src.loadData("time_series_covid19_recovered_global.csv", "CumRecovered"))

countries = allData['Country/Region'].unique()
countries.sort()

external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
tickFont = {'size':12, 'color':"rgb(30,30,30)", \
            'family':"Courier New, monospace"}


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    style={ 'font-family':"Courier New, monospace" }, 
    children=[
        ## 
        html.H1('Case History of the Coronavirus (COVID-19)'),
        html.Div(className="row", children=[
            html.Div(className="four columns", children=
                html.H5('Country'),
                dcc.Dropdown( 
                    id='country',
                    options=[{'label':c, 'value':c} \
                        for c in countries],
                    value='India'
                )
            ]),
            html.Div(className="four columns", children=[
                html.H5('State / Province'),
                dcc.Dropdown(
                    id='state'
                )
            ]),
            html.Div(className="four columns", children=[
                html.H5('Selected Metrics'),
                dcc.Checklist(
                    id='metrics',
                    options=[{'label':m, 'value':m} for m in \
                        ['Confirmed', 'Deaths', 'Recovered']],
                    value=['Confirmed', 'Deaths']
                )
            ])
        ]),
    ]
)



@app.callback(
    Output('plot_new_metrics', 'figure'), 
    [Input('country', 'value'), Input('state', 'value'), 
     Input('metrics', 'value')]
)
def update_plot_new_metrics(country, state, metrics):
    data = nonreactive_data(country, state)
    return barchart(data, metrics, prefix="New", 
        yaxisTitle="New Cases per Day")
@app.callback(
    Output('plot_cum_metrics', 'figure'), 
    [Input('country', 'value'), Input('state', 'value'), 
     Input('metrics', 'value')]
)
def update_plot_cum_metrics(country, state, metrics):
    data = nonreactive_data(country, state)
    return barchart(data, metrics, prefix="Cum", 
        yaxisTitle="Cumulated Cases")


@app.callback(
    [Output('state', 'options'), Output('state', 'value')],
    [Input('country', 'value')]
)
def update_states(country):
    states = list(allData.loc[allData['Country/Region'] == country]
        ['Province/State'].unique()
    )
    states.insert(0, '<all>')
    states.sort()
    state_options = [{'label':s, 'value':s} for s in states]
    state_value = state_options[0]['value']
    return state_options, state_value

colors = { 'Deaths':'rgb(200,30,30)', \
           'Recovered':'rgb(30,200,30)', \ 
           'Confirmed':'rgb(100,140,240)' }
def barchart(data, metrics, prefix="", yaxisTitle=""):
    figure = go.Figure(data=[
        go.Bar(
            name=metric, x=data.date, y=data[prefix + metric],
            marker_line_color='rgb(0,0,0)', marker_line_width=1,
            marker_color=colors[metric]
        ) for metric in metrics
    ])
    figure.update_layout( 
              barmode='group', legend=dict(x=.05, y=0.95), 
              plot_bgcolor='#FFFFFF', font=tickFont) \
          .update_xaxes( 
              title="", tickangle=-90, type='category',  
              showgrid=True, gridcolor='#DDDDDD', 
              tickfont=tickFont, ticktext=data.dateStr,                     
              tickvals=data.date) \
          .update_yaxes(
              title=yaxisTitle, showgrid=True, gridcolor='#DDDDDD')
    return figure

def nonreactive_data(country, state):
    data = allData.loc[allData['Country/Region'] == country] \
                  .drop('Country/Region', axis=1)
    if state == '<all>':
        data = data.drop('Province/State', axis=1) \
                   .groupby("date") \
                   .sum() \
                   .reset_index()
    else:
       data = data.loc[data['Province/State'] == state]
    newCases = data.select_dtypes(include='Int64').diff().fillna(0)
    newCases.columns = [column.replace('Cum', 'New') 
                        for column in newCases.columns]
    data = data.join(newCases)
    data['dateStr'] = data['date'].dt.strftime('%b %d, %Y')
    return 
    
