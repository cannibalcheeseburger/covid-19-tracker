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
import os

time_series  = src.case_time_series()
state_total,last_update = src.states_wise()
state_daily = src.daily_state()
state_cumu  = src.state_cumu()
state_codes_zip = zip(state_total.State.unique(), state_total.State_code.unique())
state_codes = dict(zip(state_total.State_code.unique(),state_total.State.unique()))


external_stylesheets = []
tickFont = {'size':12, 'color':"rgb(30,30,30)", \
            'family':"Courier New, monospace"}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}])

app.title =  'Covid-19 Tracker'

app._favicon = 'img/favicon.png'


                                    #'''Scatter Plot'''#
state_scatter = px.scatter(state_total[1:], x='Confirmed', y='Deaths', size_max=150,
                        size='Confirmed', color='State',log_x=True)
state_scatter.update_layout(plot_bgcolor='#003f5c',
                        xaxis=dict(showline=False,showgrid=False,zeroline=False),
                        yaxis=dict(showline=False, showgrid=False,zeroline=False),
                            title={
                            'text': 'Relation b/w Deaths and Confirmed Cases',
                            'y': 0.95,
                            'x': 0.4,
                            'xanchor': 'center',
                            'yanchor': 'top'}
                        )


app.layout = html.Div( children  = [
    html.H1(children = "Covid-19 Tracker", id = 'h1id',className='heading'),

    html.P(id = 'last_update',children = "LAST UPDATED: "+str(last_update), className='last_update'),
    
    html.Div([
        dcc.Dropdown(
            id = 'dropdown',
            className='custom_dropdown',
            options=[{'label': i, 'value': j} for i,j in state_codes_zip],
            value='TT'
        ),

    ]),      
      
    html.Div([
        dcc.Tabs(parent_className='custom_tabs',
                 className='custom_tabs_container', children=[
            dcc.Tab(label='Total Cases', className='custom_tab',selected_className='selected_custom_tab',children=[
                dcc.Graph(
                    id='time_series_total',
                    className='graph',
                    config={'displayModeBar': False}
                ),

            ]),
            dcc.Tab(label='Daily Cases', className='custom_tab', selected_className='selected_custom_tab', children=[
                dcc.Graph(
                    id='time_series_daily',
                    className='graph',
                    config={'displayModeBar': False}
                )

            ])
            
        ])
    ]),

    html.Div(children=[
        dcc.Graph(
            id='state_scatter_graph',
            className='graph',
            figure=state_scatter,
            config={'displayModeBar': False}
        ),
    ]),    
])   



@app.callback(
              [Output('time_series_total', 'figure'),
               Output('time_series_daily', 'figure')],

              [Input('dropdown', 'value')])

def update_graph(drop_value):
    
    figure_total = go.Figure()
    figure_daily=go.Figure()
    if drop_value == 'TT':

        figure_total.add_trace(go.Scatter(x=time_series['Date'],y=time_series['Total Confirmed'],mode='lines',name='Total Confirmed',text="Confirmed"))
        figure_total.add_trace(go.Scatter(x=time_series['Date'], y=time_series['Total Recovered'], mode='lines', name='Total Recovered',line_color='#00ff00'))
        figure_total.add_trace(go.Scatter(x=time_series['Date'], y=time_series['Total Deceased'], mode='lines', name='Total Deceased',line_color='#ff0000'))
        
        figure_daily.add_trace(go.Scatter(
               x = time_series['Date'], y = time_series['Daily Confirmed'], mode = 'lines', name = 'Daily Confirmed'))
        figure_daily.add_trace(go.Scatter(
               x = time_series['Date'], y = time_series['Daily Recovered'], mode = 'lines', name = 'Daily Recovered', line_color = '#00ff00'))
        figure_daily.add_trace(go.Scatter(
               x = time_series['Date'], y = time_series['Daily Deceased'], mode = 'lines', name = 'Daily Deceased', line_color = '#ff0000'))

    else:

        confirmed_cumu = state_cumu[state_cumu['Status'] == 'Confirmed']
        deceased_cumu = state_cumu[state_cumu['Status'] == 'Deceased']
        recovered_cumu = state_cumu[state_cumu['Status'] == 'Recovered']

        figure_total.add_trace(go.Scatter(
                x=confirmed_cumu['Date'], y=confirmed_cumu[drop_value], mode='lines', name='Total Confirmed'))
        figure_total.add_trace(go.Scatter(
                x=recovered_cumu['Date'], y=recovered_cumu[drop_value], mode='lines', name='Total Recovered', line_color='#00ff00'))
        figure_total.add_trace(go.Scatter(
                x=deceased_cumu['Date'], y=deceased_cumu[drop_value], mode='lines', name='Total Deceased', line_color='#ff0000'))

        confirmed_daily=state_daily[state_daily['Status']== 'Confirmed']
        recovered_daily=state_daily[state_daily['Status']== 'Recovered']
        deceased_daily=state_daily[state_daily['Status']== 'Deceased']

        figure_daily.add_trace(go.Scatter(
                x = confirmed_daily['Date'], y = confirmed_daily[drop_value], mode = 'lines', name = 'Daily Confirmed'))
        figure_daily.add_trace(go.Scatter(
                x = recovered_daily['Date'], y = recovered_daily[drop_value], mode = 'lines', name = 'Daily Recovered', line_color = '#00ff00'))
        figure_daily.add_trace(go.Scatter(
                x = deceased_daily['Date'], y = deceased_daily[drop_value], mode = 'lines', name = 'Daily Deceased', line_color = '#ff0000'))

    figure_total.update_layout(plot_bgcolor="#f5f5f5",
                                   xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False),
                                   title={'text': 'Total Cases in %s' % (
                                       state_codes['%s' % drop_value]), 'xanchor': 'center', 'x': 0.5},
                                   xaxis_title="Date",
                                   yaxis_title="Cases",
                                   xaxis_range=['2020-04-01',
                                                max(time_series['Date'])],
                                   showlegend=False,
                                   )
        
    figure_daily.update_layout(plot_bgcolor='#f5f5f5',
                                   xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False),
                                   title={'text': 'Daily Cases in %s' % (
                                       state_codes['%s' % drop_value]), 'xanchor': 'center', 'x': 0.5},
                                   xaxis_title="Date",
                                   yaxis_title="Cases",
                                   xaxis_range=['2020-04-01',
                                                max(time_series['Date'])],
                                   showlegend=False,)

    return figure_total, figure_daily 

server = app.server

if __name__ == "__main__":
    app.run_server(debug = True)
