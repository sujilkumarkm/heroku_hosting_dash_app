#import packages to create app
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from gapminder import gapminder

import plotly.express as px
import pandas as pd
import numpy as np



#get unique continents
cont_names = gapminder['continent'].unique()
cols=list(gapminder.columns)
#data for the region plot
loc_data = px.data.gapminder()
loc_cols=list(loc_data.columns)



# needed only if running this as part of a multipage app
from app import app
#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#bfbfbf',
    'text': '#1c1cbd'
}
color_discrete_map = {'Asia': '#636EFA', 'Africa': '#EF553B', 'Americas': '#00CC96',
    'Europe': '#AB63FA', 'Oceania': '#FFA15A'}


# change to app.layout if running as single page app instead
layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('Global Gapminder Data',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #Add multiple line text 
    html.Div('''
        Life Expectancy vs GDP per Capita for different Countries from 1952 to 2007 
    ''', style={
        'textAlign': 'center',
        'color': colors['text']}
    ),
    html.Div([
        html.Div([
            html.Label('Select Continent/Continents'),
            dcc.Dropdown(id='cont_dropdown',
                        options=[{'label': i, 'value': i}
                                for i in cont_names],
                        value=['Asia','Europe','Africa','Americas','Oceania'],
                        multi=True
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Select Population Range'),
                dcc.RangeSlider(id='pop_range',
                    min=60011,
                    max=1318683096,
                    value=[60011,1318683096],
                    step= 1,
                    marks={
                        60011: '60K',
                        100000000: '100M',
                        500000000: '500M',
                        1318683096: '1320M'
                    },
                )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ]),
    dcc.Graph(
        id='LifeExpVsGDP'
    ),
    html.Label('Select Variable to display on Graphs'),
        dcc.Dropdown(id='y_dropdown',
            options=[                    
                {'label': 'Life Expectancy', 'value': 'lifeExp'},
                {'label': 'Population', 'value': 'pop'},
                {'label': 'GDP per Captia', 'value': 'gdpPercap'}],
            value='lifeExp',
            style={'width':'50%'}
    ),
    html.Div([
        html.Div([
            dcc.Graph(
                id='LifeExp'
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='LifeExpOverTime',
            )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ])

])

@app.callback(
    Output(component_id='LifeExpVsGDP', component_property='figure'),
    [Input(component_id='cont_dropdown', component_property='value'),
    Input(component_id='pop_range', component_property='value')]
)
def update_graph(selected_cont,rangevalue):
    if not selected_cont:
        return dash.no_update
    data =[]
    d = gapminder[(gapminder['pop'] >= rangevalue[0]) & (gapminder['pop'] <= rangevalue[1])]
    for j in selected_cont:
            data.append(d[d['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    scat_fig = px.scatter(data_frame=df, x="gdpPercap", y="lifeExp",
                size="pop", color="continent",hover_name="country",
                # different colour for each country
                color_discrete_map=color_discrete_map, 
               #add frame by year to create animation grouped by country
               animation_frame="year",animation_group="country",
               #specify formating of markers and axes
               log_x = True, size_max=60, range_x=[100,100000], range_y=[28,92],
                # change labels
                labels={'pop':'Population','year':'Year','continent':'Continent',
                        'country':'Country','lifeExp':'Life Expectancy','gdpPercap':"GDP/Capita"})
    # Change the axis titles and add background colour using rgb syntax
    scat_fig.update_layout({'xaxis': {'title': {'text': 'log(GDP Per Capita)'}},
                  'yaxis': {'title': {'text': 'Life Expectancy'}}}, 
                  plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    return scat_fig



@app.callback(
    [Output(component_id='LifeExp', component_property='figure'),
    Output(component_id='LifeExpOverTime', component_property='figure')],
    [Input(component_id='cont_dropdown', component_property='value'),
    Input(component_id='pop_range', component_property='value'),
    Input(component_id='y_dropdown', component_property='value')]
)
def update_map(selected_cont,rangevalue,yvar):
    if not (selected_cont or rangevalue or yvar):
        return dash.no_update
    d = loc_data[(loc_data['pop'] >= rangevalue[0]) & (loc_data['pop'] <= rangevalue[1])]
    data =[]
    for j in selected_cont:
            data.append(d[d['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=loc_cols)
    df=df.infer_objects()
    map_fig= px.choropleth(df,locations="iso_alpha", color=df[yvar],
            hover_name="country",hover_data=['continent','pop'],animation_frame="year",    
            color_continuous_scale='Turbo',range_color=[df[yvar].min(), df[yvar].max()],
            labels={'pop':'Population','year':'Year','continent':'Continent',
                'country':'Country','lifeExp':'Life Expectancy'})
    map_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    line_fig = px.line(data_frame=df, 
                x="year",  y = df[yvar] , color='continent',line_group="country", 
                hover_data=['pop','year'],
                 # Add bold variable in hover information
                  hover_name='country',color_discrete_map=color_discrete_map,
                 # change labels
                 labels={'pop':'Population','year':'Year','continent':'Continent',
                     'country':'Country','lifeExp':'Life Expectancy'})
    line_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',
        paper_bgcolor='rgb(233, 238, 245)')
        
    return [map_fig, line_fig]

# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8097,debug=True)
