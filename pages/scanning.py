from dash import html

import dash_bootstrap_components as dbc
from dash import dcc
import plotly.express as px
from components import dataTransformation
import numpy as np

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
                    },
                     style={'width': '100%', 'height': '415px'}
                ) 
            ])
        ),  
    ])

def drawTabs1():
    return  html.Div([        
        dbc.Card([
            dbc.CardHeader(
                dbc.Tabs(
                    [
                        dbc.Tab(label="Map", tab_id="tab-1"),
                        dbc.Tab(label="Tab 2", tab_id="tab-2"),
                    ],
                    id="card-tabs-1",
                    active_tab="tab-1",
                )
            ),
            dbc.CardBody(html.Div(id="card-content-1")),
        ],style={"height":"34rem"})  
    ])

def drawTabs2():
    return  html.Div([        
        dbc.Card([
            dbc.CardHeader(
                dbc.Tabs(
                    [
                        dbc.Tab(label="Dataset", tab_id="tab-1"),
                        dbc.Tab(label="Tab 2", tab_id="tab-2"),
                    ],
                    id="card-tabs-2",
                    active_tab="tab-1",
                )
            ),
            dbc.CardBody(html.Div(id="card-content-2")),
        ],style={"height":"34rem"})  
    ])


SPAN_STYLE={
    "textAlign":"center",
    "backgroundColor": "#f8f9fa",
}

INPUT_NUMBER_STYLE={
    "width": "3rem",  # Personaliza el ancho del campo
    "fontSize": "12px",  # Personaliza el tamaño de fuente
    
}

def drawSlider(name,sliderid,numberid,value,min,max,step):
    return html.Div([
        dbc.Col([
                    html.Div([
                        html.P([
                            html.Span(name)
                        ]),                        
                    ],style=SPAN_STYLE),
                    dbc.Row([
                        dbc.Col([
                            dcc.Slider(min=min, max=max, step=step,
                            value=value,
                            id=sliderid,
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}
                            ),                            
                        ],width=10),                        
                        dbc.Col([
                            dcc.Input(
                            id=numberid,
                            type="number",
                            style=INPUT_NUMBER_STYLE,
                            value=value                            
                            )
                        ],width=2),
                    ])
                ]),
    ])

def drawCotrs():
    return html.Div([
        html.Div([
            html.P([
                html.Span("Controls Map")
            ],style=SPAN_STYLE),
            
        ]),
        
        html.Div([            
            dbc.Row([
                dbc.Col([
                    drawSlider("Radio","idRadioSlider","idRadioNumber",16,15,20,0.2)
                ]),
                dbc.Col([
                    drawSlider("Zoom","idZoomSlider","idZoomNumber",16,15,17,0.1)
                ]),

            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawSlider("Opacity","idOpacitySlider","idOpacityNumber",15,1,30,1)
                ]),
                dbc.Col([                    
                    html.Div([
                        html.P([
                            html.Span("Data filters")
                        ]),                        
                    ],style=SPAN_STYLE),
                    html.Div([
                        html.P([
                            html.Span("Control entities")
                        ]),                        
                    ]),
                    dcc.Checklist(
                        np.insert(dataTransformation.entities, 0, "All"),
                        ["All"],
                        id='entitiesChecklist',
                        inline=True,
                        labelStyle={'display': 'inline-block', 'marginRight': '1rem'},
                    ),
                    html.Br(),
                    html.Div([
                        html.P([
                            html.Span("Data grouping")
                        ]),                        
                    ]),
                    dcc.Dropdown(
                        id='idDataGrouping', 
                        options=['Hourly','Diary', 'Weekly', 'Monthly','All'], 
                        value='All'
                                                                     
                    ),
                    html.Br(),
                    html.Div([
                        html.P([
                            html.Span("Time's window")
                        ]),                        
                    ]),
                    dcc.RangeSlider(min=dataTransformation.startYear, 
                                    max= dataTransformation.endYear,
                                    step=1,value=[dataTransformation.startYear,dataTransformation.endYear],
                                    id='idrangeslider', 
                                    marks=None,  
                                    tooltip={"placement": "bottom", "always_visible": True} 
                                    ), 
                    html.Br(),
                    html.Div([
                        html.P([
                            html.Span("Particular grouping")
                        ]),                        
                    ]),
                    dcc.Dropdown(
                        id='idParticularGrouping', 
                        options=[''],
                        value=''
                    ),
                    html.Br(),
                ])
                
            ])
        ])

    ])

# Data
df = px.data.iris()    


def layout():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([drawTabs1()],width=8),
                    dbc.Col([drawTabs2()],width=4),
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([drawCotrs()],width=8), 
                    dbc.Col([drawFigure()],width=4),                                   
                    
                ])
            ])
        )
    ])


