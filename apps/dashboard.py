#import packages to create app
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from gapminder import gapminder

import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('E:\\Data_Visualization\\data_visualisation_ca2_dkit\\cleaned_data.csv')
columns=list(df.columns)
county_names = df['county'].unique()


# needed only if running this as part of a multipage app
from app import app
#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#bfbfbf',
    'text': '#1c1cbd'
}
color_discrete_map = {'Cavan': '#636EFA', 'Armagh': '#EF553B', 'Down': '#00CC96',
    'Dublin': '#AB63FA', 'Kerry': '#FFA15A'}



layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('Gealic Match Analysis',
        style={
            'textAlign': 'center',
            'color': '#1c1cbd',
            }
            ),
            html.Div([
            html.Label('Select Counties'),
            dcc.Dropdown(id='county_drop',
                        options=[{'label': i, 'value': i}
                                for i in county_names],
                        value=['Cavan', 'Armagh', 'Down', 'Dublin', 'Kerry'],
                        multi=True
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
        html.Label('Select Build Up Pass Range'),
        dcc.RangeSlider(id='pass_range',
            min=0,
            max=29,
            value=[0,29],
            step= 1,
            marks={
                0: '0',
                10: '10',
                20: '20',
                30: '30',
            },
        )
],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                dcc.Graph(
        id='county_Graph'
    ),

])
@app.callback(
    Output(component_id='county_Graph', component_property='figure'),
    [Input(component_id='county_drop', component_property='value'),
     Input(component_id='pass_range', component_property='value')]
)
def update_graph(selected_cont,rangevalue):
    if not selected_cont:
        return dash.no_update
    data =[]
    d = df[(df['build_up_passes'] >= rangevalue[0]) & (df['distance_from_goal'] <= rangevalue[1])]
    for j in selected_cont:
            data.append(d[d['county'] == j])
   
    df=df.infer_objects()
    scat_fig = px.scatter(data_frame=df, x="distance_from_goal", y="angle",
                size="county", color="county",hover_name="county",
                # different colour for each country
                # color_discrete_map=color_discrete_map, //////////// 
               #add frame by year to create animation grouped by country
            #    animation_frame="shot_id",animation_group="county", /////////////
               #specify formating of markers and axes
            #    log_x = True, size_max=60, range_x=[100,100000], range_y=[28,92],
                # change labels
                labels={'pop':'Population','year':'Year','continent':'Continent',
                        'country':'Country','lifeExp':'Life Expectancy','gdpPercap':"GDP/Capita"})
    # Change the axis titles and add background colour using rgb syntax
    scat_fig.update_layout({'xaxis': {'title': {'text': 'log(GDP Per Capita)'}},
                  'yaxis': {'title': {'text': 'Life Expectancy'}}}, 
                  plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    return scat_fig