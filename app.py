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
import dash_bootstrap_components as dbc
import json
from urllib.request import urlopen


df,last_update= src.states_wise()
with open('lol.geojson') as f:
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
                            columns=[{"name":i,"id":i} for i in state_total.drop(0).columns[:5]],
                            data=state_total.drop(0).to_dict('records'),
                            style_cell={'backgroundColor':'#fafafa'},
                            style_header={'backgroundColor': '#ffffff','textAlign':'center','fontWeight':'bold'},
                            style_data={'border':'2px white',},
                            style_data_conditional=[
                            {
                                # stripped rows
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#ffffff'
                            },
                            ],
                            style_as_list_view = True,
                        )
                    ]),
        ]),

    ]),
]),


     html.Div(id='trends_container', children=[
            html.Div(id='spread_trends',children=[
                html.Img(src="https://phil.cdc.gov//PHIL_Images/23312/23312_lores.jpg",width='170px',height='100px',style={'marginTop':'0px'})
                ,html.H3('Spread Trends'),
            ]),
            html.Div(className='trend_confirmed',children=[
                html.H4("Confirmed"),
                html.H6("+ "+str(time_series['Daily Confirmed'].iloc[-1]))
            ])
            
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

    html.Div(id='scatter_graph_bottom',children=[
        dcc.Graph(
            id='state_scatter_graph',
            className='graph',
            figure=state_scatter,
            config={'displayModeBar': False}
        ),
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
    dcc.Graph(  id = 'choropleth',figure = px.choropleth_mapbox(df,geojson = geo, color="Confirmed",
                           locations="State",mapbox_style="carto-positron",
                           featureidkey="properties.NAME_1",
                           center={"lat": 28.5934, "lon": 77.2223},zoom=3,color_continuous_scale='Rainbow', range_color=[0,400000])
    )
        
])   

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


        figure_confirmed.update_traces(marker_line_color='rgb(255,7,58)',marker_line_width=3,opacity=0.4)
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
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Confirmed<br>%s"%time_series['Total Confirmed'].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])

        figure_recovered.update_traces(marker_line_color='rgb(0,220,0)',marker_line_width=3, opacity=0.4)
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
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Recovered<br>%s"%time_series['Total Recovered'].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])

        figure_deceased.update_traces(marker_line_color='rgb(153, 141, 141)',marker_line_width=3, opacity=0.4)                               
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
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Deceased<br>%s"%time_series['Total Deceased'].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])


        return figure_confirmed, figure_recovered, figure_deceased 


    if drop_value=='TT' and value=='daily':
        figure_confirmed=go.Figure(go.Bar(x=time_series['Date'],y=time_series['Daily Confirmed'],width=0.4))
        figure_recovered=go.Figure(go.Bar(x=time_series['Date'],y=time_series['Daily Recovered'],width=0.4))
        figure_deceased=go.Figure(go.Bar(x=time_series['Date'],y=time_series['Daily Deceased'],width=0.4))

        figure_confirmed.update_traces(marker_line_color='rgb(255,7,58)',marker_line_width=3,opacity=0.4)
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
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Confirmed<br>%s"%time_series['Daily Confirmed'].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])

        figure_recovered.update_traces(marker_line_color='rgb(0,220,0)',marker_line_width=3, opacity=0.4)
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
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Recovered<br>%s"%time_series['Daily Recovered'].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])

        figure_deceased.update_traces(marker_line_color='rgb(153, 141, 141)',marker_line_width=3, opacity=0.4)                               
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
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Deceased<br>%s"%time_series['Daily Deceased'].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])


        return figure_confirmed, figure_recovered, figure_deceased

######################################################################################################################################3
#####################################################################################################################################3
    
    if drop_value!='TT' and value=='total':
        figure_confirmed=go.Figure(go.Bar(x=state_cumu[state_cumu['Status'] == 'Confirmed']['Date'], y=state_cumu[state_cumu['Status'] == 'Confirmed'][drop_value],width=0.4))
        figure_recovered=go.Figure(go.Bar(x=state_cumu[state_cumu['Status'] == 'Recovered']['Date'], y=state_cumu[state_cumu['Status'] == 'Recovered'][drop_value],width=0.4))
        figure_deceased=go.Figure(go.Bar(x=state_cumu[state_cumu['Status'] == 'Deceased']['Date'], y=state_cumu[state_cumu['Status'] == 'Deceased'][drop_value],width=0.4))

        figure_confirmed.update_traces(marker_line_color='rgb(255,7,58)',marker_line_width=3,opacity=0.4)
        figure_confirmed.update_xaxes(rangeslider_visible=False,rangeselector=dict(buttons=list([dict(label="All",step="all"),dict(count=4, label="4M", step="month", stepmode="backward"),dict(count=3, label="3M", step="month", stepmode="backward"),dict(count=2, label="2M", step="month", stepmode="backward"),dict(count=1, label="1M", step="month", stepmode="backward"),])))
        figure_confirmed.update_layout(plot_bgcolor="#ffffff",transition_duration=400, xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month, max(time_series['Date'])],
                                   showlegend=False,
                                   autosize=False,
                                   width=460, height=240,
                                   margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#f50000"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Confirmed<br>%s"%state_cumu[state_cumu['Status'] == 'Confirmed'][drop_value].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])

        figure_recovered.update_traces(marker_line_color='rgb(0,220,0)',marker_line_width=3, opacity=0.4)
        figure_recovered.update_xaxes(rangeslider_visible=False,rangeselector=dict(buttons=list([dict(label="All",step="all"),dict(count=4, label="4M", step="month", stepmode="backward"),dict(count=3, label="3M", step="month", stepmode="backward"),dict(count=2, label="2M", step="month", stepmode="backward"),dict(count=1, label="1M", step="month", stepmode="backward"),])))    
        figure_recovered.update_layout(plot_bgcolor='#ffffff',transition_duration=400,xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month, max(time_series['Date'])],
                                   showlegend=False,autosize=False,width=460,height=240,
                                  margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#00fd00"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Recovered<br>%s"%state_cumu[state_cumu['Status'] == 'Recovered'][drop_value].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])

        figure_deceased.update_traces(marker_line_color='rgb(153, 141, 141)',marker_line_width=3, opacity=0.4)                               
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
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Deceased<br>%s"%state_cumu[state_cumu['Status'] == 'Deceased'][drop_value].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])


        return figure_confirmed, figure_recovered, figure_deceased


    if drop_value!='TT' and value=='daily':
        figure_confirmed=go.Figure(go.Bar(x=state_daily[state_daily['Status'] == 'Confirmed']['Date'], y=state_daily[state_daily['Status'] == 'Confirmed'][drop_value],width=0.4))
        figure_recovered=go.Figure(go.Bar(x=state_daily[state_daily['Status'] == 'Recovered']['Date'], y=state_daily[state_daily['Status'] == 'Recovered'][drop_value],width=0.4))
        figure_deceased=go.Figure(go.Bar(x=state_daily[state_daily['Status'] == 'Deceased']['Date'], y=state_daily[state_daily['Status'] == 'Deceased'][drop_value],width=0.4))

        figure_confirmed.update_traces(marker_line_color='rgb(255,7,58)',marker_line_width=3,opacity=0.4)
        figure_confirmed.update_xaxes(rangeslider_visible=False,rangeselector=dict(buttons=list([dict(label="All",step="all"),dict(count=4, label="4M", step="month", stepmode="backward"),dict(count=3, label="3M", step="month", stepmode="backward"),dict(count=2, label="2M", step="month", stepmode="backward"),dict(count=1, label="1M", step="month", stepmode="backward"),])))
        figure_confirmed.update_layout(plot_bgcolor="#ffffff",transition_duration=400, xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month, max(time_series['Date'])],
                                   showlegend=False,
                                   autosize=False,
                                   width=460, height=240,
                                   margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#f50000"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Confirmed<br>%s"%state_daily[state_daily['Status'] == 'Confirmed'][drop_value].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])

        figure_recovered.update_traces(marker_line_color='rgb(0,220,0)',marker_line_width=3, opacity=0.4)
        figure_recovered.update_xaxes(rangeslider_visible=False,rangeselector=dict(buttons=list([dict(label="All",step="all"),dict(count=4, label="4M", step="month", stepmode="backward"),dict(count=3, label="3M", step="month", stepmode="backward"),dict(count=2, label="2M", step="month", stepmode="backward"),dict(count=1, label="1M", step="month", stepmode="backward"),])))    
        figure_recovered.update_layout(plot_bgcolor='#ffffff',transition_duration=400,xaxis=dict(showline=False, showgrid=False),
                                   yaxis=dict(showline=False, showgrid=False,side='right'),
                                   xaxis_range=[last_month, max(time_series['Date'])],
                                   showlegend=False,autosize=False,width=460,height=240,
                                  margin=dict(l=0,r=50,b=50,t=50,pad=5),
                                   font=dict(family="Sans Serif", size=9, color="#00fd00"),
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Recovered<br>%s"%state_daily[state_daily['Status'] == 'Recovered'][drop_value].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])

        figure_deceased.update_traces(marker_line_color='rgb(153, 141, 141)',marker_line_width=3, opacity=0.4)                               
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
                                   annotations=[dict(x=0,y=1,showarrow=False,text="Deceased<br>%s"%state_daily[state_daily['Status'] == 'Deceased'][drop_value].iloc[-1], font =dict(size = 16),xref="paper",yref="paper")])


        return figure_confirmed, figure_recovered, figure_deceased

server = app.server

if __name__ == "__main__":
    app.run_server(debug = True)