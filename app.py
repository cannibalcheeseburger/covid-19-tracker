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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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


app.layout = html.Div(children = [
    html.H1(children = "Covid-19Tracker", id = 'h1id'),

    html.P(id = 'last',children = "LAST UPDATED: "+str(last_update)),

    html.Div(id = 'left_fix_container',children = [
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
        html.Div(id='StatusActive', children=[
            html.H5('Active'),
            html.H6('‎'),
            html.H4(state_total['Active'].iloc[0]),
            
        ]),

    html.Div(children=[
        dcc.Loading(color = '#ffffff', children = [
            html.Div([
                        dash_table.DataTable(
                            id='left_table',
                            columns=[{"name":i,"id":i} for i in state_total.columns[:5]],
                            data=state_total.to_dict('records'),
                            style_cell={'backgroundColor':'#fafafa'},
                            style_header={'backgroundColor': '#ffffff','textAlign':'center','fontWeight':'bold'},
                            style_data={'border':'2px white',},
                            style_data_conditional=[
                            {
                                # stripped rows
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#ffffff'
                            },
                            {
                                'if': {'column_id': ['State','Recovered','Deaths','Confirmed','Active']},
                                'textAlign': 'center',
                                'fontWeight':'bold',
                                
                                'maxWidth':'100px',
                                
                                
                            },
                            ],
                            style_as_list_view = True,
                        )
                    ]),
        ]),

    ]),

    ]),


    html.Div(id='right_container', children=[
        html.Div(id = 'dropdown_top',children = [
            dcc.Dropdown(
                id = 'dropdown',
                className='custom_dropdown',
                options=[{'label': i, 'value': j} for i,j in state_codes_zip],
                value='TT'
            ),

        ]),      

        html.Div(className='graph_right_side', children=[
            dcc.Graph(
                id='time_series_total',
                className='graph',
                config={'displayModeBar': False}

            ),

            dcc.Graph(
                id='time_series_daily',
                className='graph',
                config={'displayModeBar': False}
            ),
        ]),

    ]),

    html.Div(id='scatter_graph_bottom',children=[
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
    figure_daily = go.Figure()
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

        figure_total.add_trace(go.Scatter(
            x=state_cumu[state_cumu['Status'] == 'Confirmed']['Date'], y=state_cumu[state_cumu['Status'] == 'Confirmed'][drop_value], mode='lines', name='Total Confirmed'))
        figure_total.add_trace(go.Scatter(
            x=state_cumu[state_cumu['Status'] == 'Deceased']['Date'], y=state_cumu[state_cumu['Status'] == 'Deceased'][drop_value], mode='lines', name='Total Recovered', line_color='#00ff00'))
        figure_total.add_trace(go.Scatter(
            x=state_cumu[state_cumu['Status'] == 'Recovered']['Date'], y=state_cumu[state_cumu['Status'] == 'Recovered'][drop_value], mode='lines', name='Total Deceased', line_color='#ff0000'))


        figure_daily.add_trace(go.Scatter(
            x=state_daily[state_daily['Status'] == 'Confirmed']['Date'], y=state_daily[state_daily['Status'] == 'Confirmed'][drop_value], mode='lines', name='Daily Confirmed'))
        figure_daily.add_trace(go.Scatter(
            x=state_daily[state_daily['Status'] == 'Recovered']['Date'], y=state_daily[state_daily['Status'] == 'Recovered'][drop_value], mode='lines', name='Daily Recovered', line_color='#00ff00'))
        figure_daily.add_trace(go.Scatter(
            x=state_daily[state_daily['Status'] == 'Deceased']['Date'], y=state_daily[state_daily['Status'] == 'Deceased'][drop_value], mode='lines', name='Daily Deceased', line_color='#ff0000'))

    figure_total.update_layout(plot_bgcolor="#ffffff",
                                    transition_duration=500,
                                   xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False),
                                   #title={'text': 'Total Cases in %s' % (
                                   #   state_codes['%s' % drop_value]), 'xanchor': 'center', 'x': 0.5,
                                   #  'yanchor':'bottom', 'y':1, 'yref':'paper'},
                                   xaxis_range=['2020-04-01',
                                                max(time_series['Date'])],
                                   showlegend=False,
                                   autosize=False,
                                   width=650, height=280,
                                   margin=dict(l=0,r=0,b=50,t=50),
                                   )
        
    figure_daily.update_layout(plot_bgcolor='#ffffff',
                                    transition_duration=500,
                                   xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False),
                                   #title={'text': 'Daily Cases in %s' % (
                                   #   state_codes['%s' % drop_value]), 'xanchor': 'center', 'x': 0.5,'yanchor':'bottom', 'y':1, 'yref':'paper'},
                                   
                                   xaxis_range=['2020-04-01',
                                                max(time_series['Date'])],
                                   showlegend=False,autosize=False,width=650,height=280,margin=dict(l=0,r=0,b=50,t=50))

    return figure_total, figure_daily 

server = app.server

if __name__ == "__main__":
    app.run_server(debug = True)
