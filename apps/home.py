import dash
from dash import html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from app import app

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            dbc.Col(html.H1("Welcome DKIT Gealic dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='This app shows the materials taught in class using Plotly, Dash and Bootstrap. '
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='It consists of two main pages: Global, which gives an overview of the overall trends from 1952 to 2007 in all countries available in the gapminder data, '
                                     'Europe, which gives an overview of the data in European countries only.')
                    , className="mb-5")
        ]),

        dbc.Row([
            # 2 columns of width 6 with a border
            dbc.Col(dbc.Card(children=[html.H3(children='Go to the original Gapminder dataset for more data',
                                               className="text-center"),
                                       dbc.Button("Gapminder Data",
                                                  href="https://www.gapminder.org/data/",
                                                  color="primary",
                                                  className="mt-3"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
                                               className="text-center"),
                                       dbc.Button("Sujil",
                                                  href="https://github.com/JackLinusMcDonnell/DashAppTeaching", target="_blank",
                                                  color="primary",
                                                  className="mt-3"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),

        ], className="mb-5"),
        dbc.Row([
            dbc.Col(html.Img(src=app.get_asset_url('hansRoslin.jpeg')), 
            width={"size": 6, "offset": 4})
        ]),
        html.A("Gaelic games (Irish: Cluichí Gaelacha) are sports played in Ireland under the auspices of the Gaelic Athletic Association (GAA). They include Gaelic football, hurling, Gaelic handball, and rounders. Women's versions of hurling and football are also played: camogie, organised by the Camogie Association of Ireland, and ladies' Gaelic football, organised by the Ladies' Gaelic Football Association.")

    ])

])