#import packages to create app
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from gapminder import gapminder

import plotly.express as px
import pandas as pd
import numpy as np

#data for the region plot
loc_data = px.data.gapminder()
loc_cols=list(loc_data.columns)
#get European data
eur_data =loc_data[loc_data['continent'] == "Europe"]
#get unique countries
country_names = eur_data['country'].unique()


color_discrete_map = {'Albania': '#000000', 'Austria': '#FFFF00', 'Belgium': '#1CE6FF',
    'Bosnia and Herzegovina': '#FF34FF','Bulgaria': '#FF4A46', 'Croatia': '#008941', 
    'Czech Republic': '#006FA6', 'Denmark': '#A30059', 'Finland': '#FFDBE5',
    'France': '#7A4900', 'Germany': '#0000A6', 'Greece': '#63FFAC', 'Hungary': '#B79762',
    'Iceland': '#8FB0FF', 'Ireland': '#004D43','Italy': '#997D87', 'Montenegro': '#5A0007',
    'Netherlands': '#809693', 'Norway': '#FEFFE6', 'Poland': '#1B4400','Portugal': '#4FC601', 
    'Romania': '#3B5DFF', 'Serbia': '#4A3B53', 'Slovak Republic': '#FF2F80', 
    'Slovenia': '#61615A','Spain': '#BA0900', 'Sweden': '#6B7900', 'Switzerland': '#00C2A0',
    'Turkey': '#FFAA92','United Kingdom': '#FF90C9'}

# needed only if running this as a single page app
from app import app
#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#e9eef5',
    'text': '#1c1cbd'
}



# change to app.layout if running as single page app instead
layout = html.Div(style={'backgroundColor': colors['background']},children=[
    dbc.Container([
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            dbc.Col(html.H1("European Gapminder Data",        
             style={
            'textAlign': 'center',
            'color': colors['text']}), 
            className="mb-5 mt-5")
        ]),
        html.Div([
            html.Div([
                html.Label('Select Country/Countries'),
                dcc.Dropdown(id='country_dropdown',
                            options=[{'label': i, 'value': i}
                                    for i in country_names],
                            value=country_names,
                            multi=True
                )
            ],style={'width': '49%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Select Population Range'),
                dcc.RangeSlider(id='eur_pop_range',
                    min=147962,
                    max=82400996,
                    value=[147962,82400996],
                    step= 1,
                    marks={
                        147962: '148K',
                        10000000: '10M',
                        50000000: '50M',
                        82400996: '82M'
                    },
                ),
                html.Label('Select Variable to display on the Graphs'),
                dcc.Dropdown(id='eur_y_dropdown',
                    options=[                    
                        {'label': 'Life Expectancy', 'value': 'lifeExp'},
                        {'label': 'Population', 'value': 'pop'},
                        {'label': 'GDP per Captia', 'value': 'gdpPercap'}],
                    value='lifeExp',
                )
            ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        ]),
        html.Div([
            dcc.Graph(
                id='barchart'
            ),
            ],style={'width': '80%', 'margin-left': '10%','display': 'inline-block'}),
        html.Div([
            html.Div([
                dcc.Graph(
                        id='geochart'
                ),
            ],style={'width': '49%','display': 'inline-block'}),
            html.Div([
                dcc.Graph(
                    id='trendline'
                ),
            ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
            ]),
    ])
])


@app.callback(
    [Output(component_id='barchart', component_property='figure'),
    Output(component_id='geochart', component_property='figure'),
    Output(component_id='trendline', component_property='figure')],
    [Input(component_id='country_dropdown', component_property='value'),
    Input(component_id='eur_pop_range', component_property='value'),
    Input(component_id='eur_y_dropdown', component_property='value')]
)
def update_graphs(selected_count,erangevalue,eyvar):
    if not (selected_count or erangevalue or eyvar):
        return dash.no_update
    d = eur_data[(eur_data['pop'] >= erangevalue[0]) & (eur_data['pop'] <= erangevalue[1])]
    data =[]
    for j in selected_count:
            data.append(d[d['country'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=loc_cols)
    df=df.infer_objects()
    barfig = px.bar(df, y=eyvar, x='country',animation_frame="year",
             # add text labels to bar
             text=eyvar, color='country', 
             # different colour for each country
             color_discrete_map=color_discrete_map,
             # Add country and life Exp info to hover text
             hover_data=['lifeExp'],
             # change labels
             labels={'pop':'Population','country':'Country','lifeExp':'Life Expectancy'})
    #update text to be number format rounded with unit 
    barfig.update_traces(texttemplate='%{text:.2s}')
    #update text to be font size 8 and hide if text can not stay with the uniform size
    barfig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
        plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
        showlegend=False, margin=dict( b=200),xaxis_title="")
    barfig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 170)
    barfig['layout']['sliders'][0]['pad']=dict(r= 10, t= 170,)
    if eyvar == 'lifeExp':
         barfig.update_yaxes(range=[0, 85])
    elif eyvar == 'pop':
         barfig.update_yaxes(range=[0, erangevalue[1]])
    else:
         barfig.update_yaxes(range=[0, 50000])

    mapfig= px.choropleth(df,locations="iso_alpha", color=df[eyvar],
            hover_name="country",hover_data=['continent','pop'],animation_frame="year",    
            color_continuous_scale='Turbo',range_color=[df[eyvar].min(), df[eyvar].max()],
            labels={'pop':'Population','year':'Year','continent':'Continent',
                'country':'Country','lifeExp':'Life Expectancy'})
    mapfig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')
    mapfig.update_geos(fitbounds="locations")
    mapfig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    linefig = px.line(data_frame=df, 
                x="year",  y = df[eyvar] , color='country',
                # different colour for each country
                color_discrete_map=color_discrete_map,
                hover_data=['pop','year'],
                 # Add bold variable in hover information
                  hover_name='country',
                 # change labels
                 labels={'pop':'Population','year':'Year','continent':'Continent',
                     'country':'Country','lifeExp':'Life Expectancy'})
    linefig.update_layout(plot_bgcolor='rgb(233, 238, 245)',
        paper_bgcolor='rgb(233, 238, 245)')
        
    return [barfig, mapfig, linefig]


# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8079,debug=True)
