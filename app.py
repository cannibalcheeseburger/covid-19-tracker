import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import src
import plotly.express as px
import json
import dash_table

time_series  = src.case_time_series()
state_total,last_update = src.states_wise()
state_daily = src.daily_state()
state_cumu  = src.state_cumu()

external_stylesheets = []
tickFont = {'size':12, 'color':"rgb(30,30,30)", \
            'family':"Courier New, monospace"}



app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.title =  'Covid-19 Tracker'

app._favicon = 'img/favicon.png'

app.layout = html.Div( children  = [
    html.H1(children = "Covid-19Tracker", id = 'h1id'),

    html.P(id = 'last',children = "LAST UPDATED: "+str(last_update)),

    html.Div(id = 'Status',children = [
        html.Div(id = 'StatusConfirmed',children =[
            html.H5('Confirmed'),
            html.H6('+ '+str(time_series['Daily Confirmed'].iloc[-1])),
            html.H4(time_series['Total Confirmed'].iloc[-1])
        ]),
        html.Div(id = 'StatusRecovered',children =[
            html.H5('Recovered'),
            html.H6('+ '+str(time_series['Daily Recovered'].iloc[-1])),
            html.H4(time_series['Total Recovered'].iloc[-1])
        ]),
        html.Div(id = 'StatusDeceased',children =[
            html.H5('Deceased'),
            html.H6('+ '+str(time_series['Daily Deceased'].iloc[-1])),
            html.H4(time_series['Total Deceased'].iloc[-1])
        ]),
    ]),
    html.Div(id="main",children=[
        dcc.Loading(color = '#161625', children = [
            html.Div([
                        dash_table.DataTable(
                            id='tables',
                            columns=[{"name":i,"id":i} for i in state_total.columns[:5]],
                            data=state_total.to_dict('records'),
                            style_header={'backgroundColor': '#1e1e30'},
                            style_cell={
                                'backgroundColor': '#1e1e30',
                                'border': '5px solid #161625',
                            },
                            style_data_conditional=[
                            {
                                # stripped rows
                                'if': {'row_index': 'even'},
                                'backgroundColor': '#161625'
                            },
                            {
                            'if': {
                                'column_id': 'State',
                            },
                            'backgroundColor': '#1e1e30',
                            },
                            ],
                        )
                    ]),
        ]),

    ]),
    html.Div(id = 'state-graph',children = [
        dcc.Dropdown(
            id = 'dropdown',
            options=[
                {'label': i, 'value': j} for i,j in zip(state_total.State.unique(),state_total.State_code.unique())
            ],
            value='TT'
        ),
        dcc.Graph(
            id = 'time-series-total',
            className = 'graph',
                ),
        dcc.Graph(
            id = 'time-series-daily',
            className = 'graph',
        )
    ]),
 
    html.Div(id = 'state-scatter',children =[
        dcc.Slider(
            id = 'mortality-slider',
            min = state_cumu['Date'].dt.month.unique().min(),
            max = state_cumu['Date'].dt.month.unique().max(),
            step = 1,
            #markers  = {i: str(i) for i in state_cumu['Date'].dt.month_name().unique()}

            #marks  ={str(j):{ 'Label': str(i)} for i,j in zip(state_cumu['Date'].dt.month_name().unique(),state_cumu['Date'].dt.month.unique())}
        ),


        dcc.Graph(
            className = 'graph',
            figure = px.scatter(state_total[1:],x = 'Deaths', y ='Confirmed',size_max=150,title='yyas',size='Deaths',color='State',log_x=True),        
            ),
        
    ]),
])


@app.callback(
    [Output('time-series-total','figure'),
    Output('time-series-daily','figure')],
    [Input('dropdown','value')]
)

def update_graph(drop_value):
    
    if drop_value == 'TT':
        figure = px.area(time_series,x = 'Date', y ='Total Confirmed',title='Time Series Total')
        figure.add_scatter( x = time_series['Date'],y=time_series['Total Deceased'],name='Deceased',fill='tozeroy')
        figure.add_scatter( x = time_series['Date'],y=time_series['Total Recovered'],name='Recovered',fill='tonexty')
        daily_fig = px.area(time_series,x = 'Date', y ='Daily Confirmed',title='Daily Time Series')   
        daily_fig.add_scatter( x = time_series['Date'],y=time_series['Daily Deceased'],name='Deceased',fill='tozeroy')
        daily_fig.add_scatter( x = time_series['Date'],y=time_series['Daily Recovered'],name='Recovered',fill='tonexty')

    else :
        figure = px.area(state_cumu[state_cumu['Status']=='Confirmed'],x = 'Date',y = drop_value,title='Daily Time Series')
        figure.add_scatter(x = state_cumu[state_cumu['Status']=='Deceased']['Date'],y = state_cumu[state_cumu['Status']=='Recovered'][drop_value],name='Recovered',fill='tonexty')
        figure.add_scatter(x =state_cumu[state_cumu['Status']=='Recovered']['Date'],y = state_cumu[state_cumu['Status']=='Deceased'][drop_value],name='Deceased',fill='tozeroy')
        daily_fig = px.area(state_daily[state_daily['Status']=='Confirmed'],x = 'Date',y = drop_value,title='Daily Time Series')
        daily_fig.add_scatter(x =state_daily[state_daily['Status']=='Deceased']['Date'],y = state_daily[state_daily['Status']=='Deceased'][drop_value],name='Deceased',fill='tozeroy')
        daily_fig.add_scatter(x = state_daily[state_daily['Status']=='Recovered']['Date'],y = state_daily[state_daily['Status']=='Recovered'][drop_value],name='Recovered',fill='tonexty')

    figure.update_layout(transition_duration=500)
    daily_fig.update_layout(transition_duration=500)

    return figure,daily_fig

server = app.server

if __name__ == "__main__":
    app.run_server(debug = True)
