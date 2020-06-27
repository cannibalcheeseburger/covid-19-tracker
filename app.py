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

external_stylesheets = ['https://raw.githubusercontent.com/plotly/dash-sample-apps/master/apps/dash-datashader/assets/style.css']
tickFont = {'size':12, 'color':"rgb(30,30,30)", \
            'family':"Courier New, monospace"}



app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.title =  'Covid-19 Tracker'

app._favicon = 'img/favicon.png'

app.layout = html.Div( children  = [
    html.H1(children = "Covid-19 Tracker", id = 'h1id'),

    html.P(id = 'last',children = "LAST UPDATED: "+str(last_update)),
    html.Div([
                dash_table.DataTable(
                    id='table',
                    columns=[{"name":i,"id":i} for i in state_total.columns[:5]],
                    data=state_total.to_dict('records'),
                    style_cell={'textAlign':'left'},
                    style_table={'height':'40%','width':'95%','margin-left':'40px','margin-up':'10px'},
                    style_data_conditional=[{
                            'if':{'row_index':'odd'},
                            'backgroundColor':'rgb(248, 248, 248)'
                    }],
                    style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                    }
                )]),
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
        dcc.Graph(
            className = 'graph',
            figure = px.scatter(state_total[1:],x = 'Deaths', y ='Confirmed',size_max=150,title='yyas',size='Deaths',color='State',log_x=True),        
            )
    ]),
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
        state_cum = state_cumu[drop_value]
        figure = px.line(state_daily[state_daily['Status']=='Confirmed'],x = 'Date',y = state_cum[::3],title='Daily Time Series')
        figure.add_scatter(x = state_daily[state_daily['Status']=='Recovered']['Date'],y = state_cum[1::3],name='Recovered')
        figure.add_scatter(x =state_daily[state_daily['Status']=='Deceased']['Date'],y = state_cum[2::3],name='Deceased')
        daily_fig = px.line(state_daily[state_daily['Status']=='Confirmed'],x = 'Date',y = drop_value,title='Daily Time Series')
        daily_fig.add_scatter(x = state_daily[state_daily['Status']=='Recovered']['Date'],y = state_daily[state_daily['Status']=='Recovered'][drop_value],name='Recovered')
        daily_fig.add_scatter(x =state_daily[state_daily['Status']=='Deceased']['Date'],y = state_daily[state_daily['Status']=='Deceased'][drop_value],name='Deceased')

    figure.update_layout(transition_duration=500)
    daily_fig.update_layout(transition_duration=500)

    return figure,daily_fig

server = app.server

if __name__ == "__main__":
    app.run_server(debug = True)
