import pandas as pd

import folium
from folium.plugins import HeatMap
from branca.element import Figure
from collections import defaultdict
import branca.colormap as cm

from dash import html, dcc
import plotly.express as px

#Importamos el documento
DTBpath= "data\DTBTraining.csv"
CRUEpath = "data\CRUETraining.csv"
Cornerspath = "data\corners.csv"

#Abrimos el documento
dfDTB=pd.read_csv(DTBpath)
dfCRUE=pd.read_csv(CRUEpath)
dfCorners=pd.read_csv(Cornerspath)

trdf=  pd.concat([dfDTB, dfCRUE])

trdf['Date']= pd.to_datetime(trdf['Date'],dayfirst=False)

trdf = trdf.sort_values('Date')

trdf = trdf.reset_index(drop=True)

trdf_copy = trdf.copy()

entities= trdf_copy['Data Entity'].unique()


startYear= trdf_copy['Date'].iloc[1].year
endYear=trdf_copy['Date'].iloc[-1].year


#Definimos el centro del mapa
centro_bmanga = [ dfCorners['Latitude'].mean(),dfCorners['Longitude'].mean()]

def colorBar(colormap):
    steps=100
    gradient_map=defaultdict(dict)
    for i in range(steps):
        gradient_map[1/steps*i] = colormap.rgb_hex_str(1/steps*i) 
    return gradient_map

def  heatmap (radio,zoom,opacity):
    colormap_view = cm.LinearColormap(colors=['blue','white','red'], vmin=dfCorners['Intensity'].min(), vmax=dfCorners['Intensity'].max())
    colormap = cm.LinearColormap(colors=['blue','white','red'], vmin=0, vmax=1)
    gradient_map=colorBar(colormap)

    m = folium.Map(centro_bmanga, zoom_start=zoom)
    fig = Figure(width=800, height=600)
    fig.add_child(m)
    heatmap = HeatMap(
        data = dfCorners[['Latitude','Longitude','Intensity']],
        name = "Emergencias",
        radius = radio,
        blur = opacity,
        gradient=gradient_map 
    )
    heatmap.add_to(m)
    colormap_view.add_to(m)
    m.save('heatmap.html')

    return html.Div([html.Iframe(id='map', srcDoc = open('heatmap.html','r').read(), width='100%', height= '460px')])

def timeSeries():
    return html.Div([
        dcc.Graph(
        id="time-series-chart",
        figure= px.line(trdf_copy,x='Date',y='Intersection Id')
        )
    ])

def histogram(datagroup):
    filter="Year"
    if(datagroup == "Diary"):
        filter="DayOfWeek"
    if(datagroup == "Weekly"):
        filter="WeekOfYear"
    if(datagroup == "Monthly"):
        filter="Month"
    if(datagroup == "Hourly"):
        filter="Hour"
    


    return html.Div([
        dcc.Graph(
            id='histogram',
            figure= px.histogram(trdf_copy, x=filter, color="Data Entity")
        )
    ])