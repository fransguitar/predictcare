import dash 
import dash_bootstrap_components as dbc
from dash import html, dash_table
from dash.dependencies import Input, Output
from dash import dcc
from pages import scanning
from components import dataTransformation

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server


MENU_STYLE = {    
    "padding": "1em",
}

userSection= dbc.Row(
    [
        dbc.Col(html.A(html.Img(src='assets/static/bell.png', height='27px'), style= MENU_STYLE)),
        dbc.Col(html.A(html.Img(src='assets/static/profile.png', height='40px'), style= MENU_STYLE)),
        
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navBar = dbc.Navbar(    
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.A(html.Img(src='assets/static/uis-logo.svg', height='35px', id="btn_sidebar"), style= MENU_STYLE)),
                        #dbc.Col(dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar")),
                        dbc.Col(dbc.NavbarBrand("PredicCare", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                #href="https://plotly.com",
                #style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            
            dbc.Collapse(
                userSection,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ,
     fluid=True,
        
    ),
     
    color="dark",
    dark=True,

)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "zIndex": 1,
    "overflowX": "auto",
    "overflowY": "auto",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "backgroundColor": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink([
                    html.A(html.Img(src='assets/static/home.png', height='25px', id="btn_sidebar"), style={"marginRight": "0.5rem"}),
                    "Home"
                ], href="/page-1", id="page-1-link"),
                
                dbc.NavLink([
                    html.A(html.Img(src='assets/static/dashboard.png', height='25px', id="btn_sidebar"), style={"marginRight": "0.5rem"}),
                    "exploration"
                ], href="/page-2", id="page-2-link"),
                
                dbc.NavLink([
                    html.A(html.Img(src='assets/static/chart.png', height='25px', id="btn_sidebar"), style={"marginRight": "0.5rem"}),
                    "Home"
                ], href="/page-3", id="page-3-link"),
                
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

CONTENT_STYLE = {
    "transition": "marginLeft .5s",
    "marginLeft": "16rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#f8f9fa",
    "height": "calc(100vh - 62.5px)",  # Agrega la altura para ocupar toda la ventana
    "overflowY": "scroll",

    
}
content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        navBar,
        sidebar,
        content
        
    ],
)

@app.callback(Output("page-content", "children"),[Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return scanning.layout()
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )
    
@app.callback(
    Output("card-content-1", "children"), 
    Input("card-tabs-1", "active_tab"),
    Input('idRadioSlider','value'),
    Input('idZoomSlider','value'),
    Input('idOpacitySlider','value'),
    Input('idDataGrouping','value')
)
def tab_content_1(active_tab,radio,zoom,opacity,datagroup):
    if active_tab == "tab-1":
        return dataTransformation.heatmap(radio,zoom,opacity)
    elif active_tab == "tab-2":
        return dataTransformation.histogram(datagroup)#scanning.drawFigure()

@app.callback(
    Output("card-content-2", "children"), [Input("card-tabs-2", "active_tab")]
)
def tab_content_2(active_tab):
    if active_tab == "tab-1":
        limited_data = dataTransformation.trdf.head(13)  # Limitar a los primeros 10 registros

        table = dash_table.DataTable(
            data=limited_data.to_dict('records'),
            columns=[{"name": i, "id": i} for i in limited_data.columns],
            id='tbl'
        )
        return html.Div(table, style={'overflowX': 'scroll'}),
    elif active_tab == "tab-2":
        return dataTransformation.timeSeries()

@app.callback(
    Output(component_id='idRadioSlider',component_property='value'),
    [Input(component_id='idRadioNumber',component_property='value')]
)
def RadioCalbacks(input_value):
    return input_value

@app.callback(
    Output(component_id='idZoomSlider',component_property='value'),
    [Input(component_id='idZoomNumber',component_property='value')]
)
def ZoomCallbacks(input_value):
    return input_value

@app.callback(
    Output(component_id='idOpacitySlider',component_property='value'),
    [Input(component_id='idOpacityNumber',component_property='value')]
)
def OpacityCallbacks(input_value):
    return input_value

@app.callback(
    Output(component_id='idParticularGrouping',component_property='options'),
    [Input(component_id='idDataGrouping',component_property='value')]
   
)
def particularGrouping (input_value):
    if(input_value=='All'):
        return ['']
    if(input_value=='Hourly'):
        return ['']
    if(input_value=='Diary'):
        return ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    if(input_value=='Weekly'):
        return list(map(str, range(1, 54)))
    if(input_value=='Monthly'):
        return ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']




if __name__ == '__main__':
    app.run_server(port=8060,debug=True)