from dash import html
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash import dcc
import plotly.express as px

# A few cities in Denmark.
cities = [dict(title="Aalborg", position=[57.0268172, 9.837735]),
          dict(title="Aarhus", position=[56.1780842, 10.1119354]),
          dict(title="Copenhagen", position=[55.6712474, 12.5237848])]

def drawFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])
# Data
df = px.data.iris()    
# Text field
def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])
#dl.Map(children=[dl.TileLayer()] + [dl.Marker(**city) for city in cities],
#               style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map"),    

def layout():
    return html.Div([
        dbc.Card(
        dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        drawText()
                    ], width=3),
                    dbc.Col([
                        drawText()
                    ], width=3),
                    dbc.Col([
                        drawText()
                    ], width=3),
                    dbc.Col([
                        drawText()
                    ], width=3),
                ], align='center'), 
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        drawFigure() 
                    ], width=3),
                    dbc.Col([
                        drawFigure()
                    ], width=3),
                    dbc.Col([
                        drawFigure() 
                    ], width=6),
                ], align='center'), 
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        drawFigure()
                    ], width=9),
                    dbc.Col([
                        drawFigure()
                    ], width=3),
                ], align='center'),      
            ]), color = 'dark'
        )
        
        
    ])