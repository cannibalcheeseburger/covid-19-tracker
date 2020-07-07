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
import datetime
import dateutil.relativedelta
from src.get_pretty_no import num
import dash_bootstrap_components as dbc
import json
from urllib.request import urlopen

df,last_update= src.states_wise()
with open('geojson/india.geojson') as f:
    geo = json.load(f)

today = datetime.date.today()
last_month = today + dateutil.relativedelta.relativedelta(months=-2)

time_series  = src.case_time_series()
state_total,last_update= src.states_wise()
state_daily = src.daily_state()
state_cumu  = src.state_cumu()
state_codes_zip = zip(state_total.State.unique(), state_total.State_code.unique())
state_codes = dict(zip(state_total.State_code.unique(),state_total.State.unique()))

college_an = src.announce()
who = src.get_who()
gov = src.get_go()



external_stylesheets = []
tickFont = {'size':12, 'color':"rgb(30,30,30)", \
            'family':"Courier New, monospace"}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title =  'Covid-19 Tracker'

app._favicon = 'img/favicon.png'




############################################
                                            #Map Of India   
                                                         #######################################################

map_of_india = px.choropleth_mapbox(df.drop(0),geojson = geo, color="Confirmed",
                           locations="State",
                           mapbox_style="carto-positron",
                           featureidkey="properties.NAME_1",
                           center={"lat": 22.3, "lon": 82.488860},zoom=3.5,
                           opacity=0.7,
                           color_continuous_scale='Oranges',
                           height=650,
                           )   

#######################################################################################

app.layout = html.Div(children = [
    html.H1(children = "Covid-19Tracker", id = 'h1id'),

    html.P(id = 'last',children = "LAST UPDATED: "+str(last_update)),

    html.Div(id = 'left_fix_container',children = [
        html.Div(id = 'StatusConfirmed',children =[
            html.H5('Confirmed'),
            html.H6('+ '+num(time_series['Daily Confirmed'].iloc[-1])),
            html.H4(num(time_series['Total Confirmed'].iloc[-1]))
        ]),
        html.Div(id = 'StatusRecovered',children =[
            html.H5('Recovered'),
            html.H6('+ '+num(time_series['Daily Recovered'].iloc[-1])),
            html.H4(num(time_series['Total Recovered'].iloc[-1]))
        ]),
        html.Div(id = 'StatusDeceased',children =[
            html.H5('Deceased'),
            html.H6('+ '+num(time_series['Daily Deceased'].iloc[-1])),
            html.H4(num(time_series['Total Deceased'].iloc[-1]))
        ]),
        html.Div(id='StatusActive', children=[
            html.H5('Active'),
            html.H6('‎'),
            html.H4(num(state_total['Active'].iloc[0])),
            
        ]),
    
    html.Div(children=[
        dcc.Loading(color = '#ffffff', children = [
            html.Div([
                        dash_table.DataTable(
                            id='left_table',
                            columns=[{"name":i,"id":i} for i in state_total.drop(0).columns[:5]],
                            data=state_total.drop(0).to_dict('records'),
                            style_cell={'backgroundColor':'#fafafa','textAlign':'center','height':'auto','whiteSpace':'normal'},
                            style_header={'backgroundColor': '#ffffff','textAlign':'center','fontWeight':'bold'},
                            style_data={'border':'2px white',},
                            style_data_conditional=[
                            {
                                # stripped rows
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#ffffff'
                            },
                            {
                                'if':{'column_id':'State'},
                                'maxWidth':'150px',
                                
                            }
                            ],
                            style_as_list_view = True,
                        )
                    ]),
            ]),

        ]),
    ]),


    html.Div(id='trends_container', children=[
            html.Div(id='spread_trends',children=[
                html.H3('Spread Trends'),
                
            ]),

                html.H4("Population:",id = 'pop'),
                html.H3(id = 'population'),
                html.Div(id = 'Confirmed_per',className = 'stats_card',children = [
                            html.H5('Confirmed Per Million'),
                            html.H3(id = 'Confirmed_per_head'),
                            html.P('No. of cases having virus for every million people tested.')
                        ]),
            
                html.Div(id = 'Recovery_rate',className = 'stats_card',children = [
                        html.H5('Recovery Rate'),
                        html.H3(id = 'Recovery_rate_head'),
                        html.P('No. of cases Recovered for every 100 cases.')
                        ]),

                html.Div(id = 'Active_per',className = 'stats_card',children = [
                        html.H5('Active Percentage'),
                        html.H3(id = 'Active_per_head'),
                        html.P('No. of cases active for every 100 confirmed cases.')
                        ]),
            
                html.Div(id = 'Mortality_rate',className = 'stats_card',children = [
                        html.H5('Mortality Rate'),
                        html.H3(id = 'Mortality_rate_head'),
                        html.P('No. of cases Passed Away for every 100 confirmed cases.')
                    ]),
            
                ]),
    


    html.Div(id='right_container', children=[
        html.Div(id = 'dropdown_top',children = [
            dcc.Dropdown(
                id = 'dropdown',
                className='custom_dropdown',
                options=[{'label': i, 'value': j} for i,j in state_codes_zip],
                value='TT',
                style={'fontWeight':'bold','backgroundColor':'#F0F0F0','border':'0px','borderColor':'#FFFFFF','fontFamily':'Sans Serif','fontSize':'14px'}
            ),

        ]),      

        html.Div([
            dcc.Tabs(id='tabs_top', value='total',
            children=[
                dcc.Tab(label='Total', value='total',style={'fontSize':'14px','fontFamily':'Sans Serif','fontWeight':'bold','border': '2px solid #fafafa','padding':'1px','backgroundColor': '#FAFAFA','marginTop':'4px','marginRight':'2px'},selected_style={'marginTop':'4px','marginRight':'2px','fontSize':'14px','fontWeight':'bold','border': '2px solid #f0f0f0','backgroundColor': '#F0F0F0','padding':'1px','fontFamily':'Sans Serif'}),
                dcc.Tab(label='Daily', value='daily',style={'fontSize':'14px','fontFamily':'Sans Serif','fontWeight':'bold','border': '2px solid #fafafa','padding':'1px','backgroundColor': '#FAFAFA','marginTop':'4px','marginLeft':'2px'},selected_style={'marginTop':'4px','marginLeft':'2px','fontSize':'14px','fontWeight':'bold','border': '2px solid #f0f0f0','backgroundColor': '#F0F0F0','padding':'1px','fontFamily':'Sans Serif'}),
            ],style={'height':'34px'})
        ]),

        html.Div(id='graph_right_side', children=[

            dcc.Graph(
                id='figure_confirmed',
                className='graph',
                config={'displayModeBar': False}
            ),
            dcc.Graph(
                id='figure_recovered',
                className='graph',
                config={'displayModeBar': False}
            ),
            dcc.Graph(
                id='figure_deceased',
                className='graph',
                config={'displayModeBar': False}
            ),
        ]),
    ]),

    html.Div(id='india_map',children=[
        dcc.Graph(  id = 'choropleth',figure = map_of_india,config={'displayModeBar': False}),
    ]),



    html.Div(className = 'cards',children=[

        html.Div(className = "CollegeAn",children = [   
            html.H2("NITH ANNOUNCEMENTS"),
            html.Div(children  = [
                html.Div(children = dcc.Link(ann[0],href = ann[1],target='_blank'),className = 'Card')for ann in college_an
                ])
        ]),


        html.Div(className = "Gov",children = [   
            html.H2("MoHFW Updates"),
            html.Div(children  = [
                html.Div(children = dcc.Link(go[1],href = go[2],target='_blank'),className = 'Card')for go in gov
                ])
        ]),


        html.Div(className = "WHO",children = [   
            html.H2("WHO Updates"),
            html.Div(children  = [
                html.Div(children = dcc.Link(new[1],href = new[2],target='_blank'),className = 'Card')for new in who
                ])
        ]),

    ]),

])   

#######################################################


@app.callback([Output('Confirmed_per_head','children'),
                Output('Active_per_head','children'),
                Output('Mortality_rate_head','children'),
                Output('Recovery_rate_head','children'),
                Output('population','children')],
                [Input('dropdown', 'value')]
)
def stats(drop_val):
    pm = state_total[state_total['State_code']==drop_val]
    active_per = round(pm['Active']*100/pm['Confirmed'],2)
    active_per = active_per.astype(str) +'%'
    con_per_mil = round(pm['Confirmed']*1000000/pm['Population'],2)
    rec_rate = round(pm['Recovered']*100/pm['Confirmed'],2)
    rec_rate = rec_rate.astype(str) +'%'
    mort_rate = round(pm['Deaths']*100/pm['Confirmed'],2)
    mort_rate = mort_rate.astype(str) +'%'
    pop = num(int(pm['Population']))
    return con_per_mil,active_per,mort_rate,rec_rate,pop


@app.callback(
              [Output('figure_confirmed', 'figure'),
               Output('figure_recovered', 'figure'),
               Output('figure_deceased', 'figure')],
               
                [Input('dropdown', 'value'),
                Input('tabs_top','value')])

def update_graph(drop_value, value):
    
    
    if drop_value == 'TT' and value=='total':

        figure_confirmed=go.Figure(go.Bar(x=time_series['Date'],y=time_series['Total Confirmed'],width=0.4))
        figure_recovered=go.Figure(go.Bar(x=time_series['Date'],y=time_series['Total Recovered'],width=0.4))
        figure_deceased=go.Figure(go.Bar(x=time_series['Date'],y=time_series['Total Deceased'],width=0.4))


        figure_confirmed.update_traces(marker_line_color='rgb(255,7,58)',marker_line_width=3,opacity=0.6)
        figure_confirmed.update_xaxes(rangeslider_visible=False,rangeselector=dict(
        buttons=list([
            dict(label="All",step="all"),
            dict(count=4, label="4M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=2, label="2M", step="month", stepmode="backward"),
            dict(count=1, label="1M", step="month", stepmode="backward"),])))
        figure_confirmed.update_layout(plot_bgcolor="#ffffff",
                                    transition_duration=400,
                                   xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month,
                                                max(time_series['Date'])],
                                   showlegend=False,
                                   autosize=False,
                                   width=460, height=240,
                                   margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#f50000"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Confirmed<br>%s"%num(time_series['Total Confirmed'].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])

        figure_recovered.update_traces(marker_line_color='rgb(0,220,0)',marker_line_width=3, opacity=0.6)
        figure_recovered.update_xaxes(rangeslider_visible=False,rangeselector=dict(
        buttons=list([
            dict(label="All",step="all"),
            dict(count=4, label="4M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=2, label="2M", step="month", stepmode="backward"),
            dict(count=1, label="1M", step="month", stepmode="backward"),])))    
        figure_recovered.update_layout(plot_bgcolor='#ffffff',
                                    transition_duration=400,
                                   xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month,
                                                max(time_series['Date'])],
                                   showlegend=False,autosize=False,width=460,height=240,
                                  margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#00fd00"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Recovered<br>%s"%num(time_series['Total Recovered'].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])

        figure_deceased.update_traces(marker_line_color='rgb(153, 141, 141)',marker_line_width=3, opacity=0.6)                               
        figure_deceased.update_xaxes(rangeslider_visible=False,rangeselector=dict(
        buttons=list([
            dict(label="All",step="all"),
            dict(count=4, label="4M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=2, label="2M", step="month", stepmode="backward"),
            dict(count=1, label="1M", step="month", stepmode="backward"),])))
        figure_deceased.update_layout(plot_bgcolor="#ffffff",
                                    transition_duration=400,
                                   xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month,
                                                max(time_series['Date'])],
                                   showlegend=False,
                                   autosize=False,
                                   width=460, height=240,
                                   margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#998d8d"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Deceased<br>%s"%num(time_series['Total Deceased'].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])


        return figure_confirmed, figure_recovered, figure_deceased 


    if drop_value=='TT' and value=='daily':
        figure_confirmed=go.Figure(go.Bar(x=time_series['Date'],y=time_series['Daily Confirmed'],width=0.4))
        figure_recovered=go.Figure(go.Bar(x=time_series['Date'],y=time_series['Daily Recovered'],width=0.4))
        figure_deceased=go.Figure(go.Bar(x=time_series['Date'],y=time_series['Daily Deceased'],width=0.4))

        figure_confirmed.update_traces(marker_line_color='rgb(255,7,58)',marker_line_width=3,opacity=0.6)
        figure_confirmed.update_xaxes(rangeslider_visible=False,rangeselector=dict(
        buttons=list([
            dict(label="All",step="all"),
            dict(count=4, label="4M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=2, label="2M", step="month", stepmode="backward"),
            dict(count=1, label="1M", step="month", stepmode="backward"),])))
        figure_confirmed.update_layout(plot_bgcolor="#ffffff",
                                    transition_duration=400,
                                   xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month,
                                                max(time_series['Date'])],
                                   showlegend=False,
                                   autosize=False,
                                   width=460, height=240,
                                   margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#f50000"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Confirmed<br>%s"%num(time_series['Daily Confirmed'].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])

        figure_recovered.update_traces(marker_line_color='rgb(0,220,0)',marker_line_width=3, opacity=0.6)
        figure_recovered.update_xaxes(rangeslider_visible=False,rangeselector=dict(
        buttons=list([
            dict(label="All",step="all"),
            dict(count=4, label="4M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=2, label="2M", step="month", stepmode="backward"),
            dict(count=1, label="1M", step="month", stepmode="backward"),])))    
        figure_recovered.update_layout(plot_bgcolor='#ffffff',
                                    transition_duration=400,
                                   xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month,
                                                max(time_series['Date'])],
                                   showlegend=False,autosize=False,width=460,height=240,
                                  margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#00fd00"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Recovered<br>%s"%num(time_series['Daily Recovered'].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])

        figure_deceased.update_traces(marker_line_color='rgb(153, 141, 141)',marker_line_width=3, opacity=0.6)                               
        figure_deceased.update_xaxes(rangeslider_visible=False,rangeselector=dict(
        buttons=list([
            dict(label="All",step="all"),
            dict(count=4, label="4M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=2, label="2M", step="month", stepmode="backward"),
            dict(count=1, label="1M", step="month", stepmode="backward"),])))
        figure_deceased.update_layout(plot_bgcolor="#ffffff",
                                    transition_duration=400,
                                   xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month,
                                                max(time_series['Date'])],
                                   showlegend=False,
                                   autosize=False,
                                   width=460, height=240,
                                   margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#998d8d"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Deceased<br>%s"%num(time_series['Daily Deceased'].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])


        return figure_confirmed, figure_recovered, figure_deceased

######################################################################################################################################3
#####################################################################################################################################3
    
    if drop_value!='TT' and value=='total':
        figure_confirmed=go.Figure(go.Bar(x=state_cumu[state_cumu['Status'] == 'Confirmed']['Date'], y=state_cumu[state_cumu['Status'] == 'Confirmed'][drop_value],width=0.4))
        figure_recovered=go.Figure(go.Bar(x=state_cumu[state_cumu['Status'] == 'Recovered']['Date'], y=state_cumu[state_cumu['Status'] == 'Recovered'][drop_value],width=0.4))
        figure_deceased=go.Figure(go.Bar(x=state_cumu[state_cumu['Status'] == 'Deceased']['Date'], y=state_cumu[state_cumu['Status'] == 'Deceased'][drop_value],width=0.4))

        figure_confirmed.update_traces(marker_line_color='rgb(255,7,58)',marker_line_width=3,opacity=0.6)
        figure_confirmed.update_xaxes(rangeslider_visible=False,rangeselector=dict(buttons=list([dict(label="All",step="all"),dict(count=4, label="4M", step="month", stepmode="backward"),dict(count=3, label="3M", step="month", stepmode="backward"),dict(count=2, label="2M", step="month", stepmode="backward"),dict(count=1, label="1M", step="month", stepmode="backward"),])))
        figure_confirmed.update_layout(plot_bgcolor="#ffffff",transition_duration=400, xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month, max(time_series['Date'])],
                                   showlegend=False,
                                   autosize=False,
                                   width=460, height=240,
                                   margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#f50000"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Confirmed<br>%s"%num(state_cumu[state_cumu['Status'] == 'Confirmed'][drop_value].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])

        figure_recovered.update_traces(marker_line_color='rgb(0,220,0)',marker_line_width=3, opacity=0.6)
        figure_recovered.update_xaxes(rangeslider_visible=False,rangeselector=dict(buttons=list([dict(label="All",step="all"),dict(count=4, label="4M", step="month", stepmode="backward"),dict(count=3, label="3M", step="month", stepmode="backward"),dict(count=2, label="2M", step="month", stepmode="backward"),dict(count=1, label="1M", step="month", stepmode="backward"),])))    
        figure_recovered.update_layout(plot_bgcolor='#ffffff',transition_duration=400,xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month, max(time_series['Date'])],
                                   showlegend=False,autosize=False,width=460,height=240,
                                  margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#00fd00"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Recovered<br>%s"%num(state_cumu[state_cumu['Status'] == 'Recovered'][drop_value].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])

        figure_deceased.update_traces(marker_line_color='rgb(153, 141, 141)',marker_line_width=3, opacity=0.6)                               
        figure_deceased.update_xaxes(rangeslider_visible=False,rangeselector=dict(
        buttons=list([dict(label="All",step="all"),dict(count=4, label="4M", step="month", stepmode="backward"),dict(count=3, label="3M", step="month", stepmode="backward"),dict(count=2, label="2M", step="month", stepmode="backward"),dict(count=1, label="1M", step="month", stepmode="backward"),])))
        figure_deceased.update_layout(plot_bgcolor="#ffffff",transition_duration=400,xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month, max(time_series['Date'])],
                                   showlegend=False,
                                   autosize=False,
                                   width=460, height=240,
                                   margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#998d8d"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Deceased<br>%s"%num(state_cumu[state_cumu['Status'] == 'Deceased'][drop_value].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])


        return figure_confirmed, figure_recovered, figure_deceased


    if drop_value!='TT' and value=='daily':
        figure_confirmed=go.Figure(go.Bar(x=state_daily[state_daily['Status'] == 'Confirmed']['Date'], y=state_daily[state_daily['Status'] == 'Confirmed'][drop_value],width=0.4))
        figure_recovered=go.Figure(go.Bar(x=state_daily[state_daily['Status'] == 'Recovered']['Date'], y=state_daily[state_daily['Status'] == 'Recovered'][drop_value],width=0.4))
        figure_deceased=go.Figure(go.Bar(x=state_daily[state_daily['Status'] == 'Deceased']['Date'], y=state_daily[state_daily['Status'] == 'Deceased'][drop_value],width=0.4))

        figure_confirmed.update_traces(marker_line_color='rgb(255,7,58)',marker_line_width=3,opacity=0.6)
        figure_confirmed.update_xaxes(rangeslider_visible=False,rangeselector=dict(buttons=list([dict(label="All",step="all"),dict(count=4, label="4M", step="month", stepmode="backward"),dict(count=3, label="3M", step="month", stepmode="backward"),dict(count=2, label="2M", step="month", stepmode="backward"),dict(count=1, label="1M", step="month", stepmode="backward"),])))
        figure_confirmed.update_layout(plot_bgcolor="#ffffff",transition_duration=400, xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month, max(time_series['Date'])],
                                   showlegend=False,
                                   autosize=False,
                                   width=460, height=240,
                                   margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#f50000"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Confirmed<br>%s"%num(state_daily[state_daily['Status'] == 'Confirmed'][drop_value].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])

        figure_recovered.update_traces(marker_line_color='rgb(0,220,0)',marker_line_width=3, opacity=0.6)
        figure_recovered.update_xaxes(rangeslider_visible=False,rangeselector=dict(buttons=list([dict(label="All",step="all"),dict(count=4, label="4M", step="month", stepmode="backward"),dict(count=3, label="3M", step="month", stepmode="backward"),dict(count=2, label="2M", step="month", stepmode="backward"),dict(count=1, label="1M", step="month", stepmode="backward"),])))    
        figure_recovered.update_layout(plot_bgcolor='#ffffff',transition_duration=400,xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month, max(time_series['Date'])],
                                   showlegend=False,autosize=False,width=460,height=240,
                                  margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#00fd00"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Recovered<br>%s"%num(state_daily[state_daily['Status'] == 'Recovered'][drop_value].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])

        figure_deceased.update_traces(marker_line_color='rgb(153, 141, 141)',marker_line_width=3, opacity=0.6)                               
        figure_deceased.update_xaxes(rangeslider_visible=False,rangeselector=dict(
        buttons=list([dict(label="All",step="all"),dict(count=4, label="4M", step="month", stepmode="backward"),dict(count=3, label="3M", step="month", stepmode="backward"),dict(count=2, label="2M", step="month", stepmode="backward"),dict(count=1, label="1M", step="month", stepmode="backward"),])))
        figure_deceased.update_layout(plot_bgcolor="#ffffff",transition_duration=400,xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month, max(time_series['Date'])],
                                   showlegend=False,
                                   autosize=False,
                                   width=460, height=240,
                                   margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#998d8d"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Deceased<br>%s"%num(state_daily[state_daily['Status'] == 'Deceased'][drop_value].iloc[-1]), font =dict(size = 16),xref="paper",yref="paper")])


        return figure_confirmed, figure_recovered, figure_deceased

server = app.server

if __name__ == "__main__":
    app.run_server(debug = True)