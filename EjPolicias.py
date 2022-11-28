import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats
from scipy.stats import norm
import altair as alt
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

st.title("Police Departmen Incident Report Dashboard")
st.markdown("ORO EN PAZ, FIERRO, EN GUERRA")

df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")

df2018 = pd.read_csv("Year_2018.csv")
cont2018 = df2018['Incident Day of Week'].value_counts()
df2019 = pd.read_csv("Year_2019.csv")
cont2019 = df2019['Incident Day of Week'].value_counts()
df2020 = pd.read_csv("Year_2020.csv")
cont2020 = df2020['Incident Day of Week'].value_counts()
dfpastel = df['Resolution'].value_counts()

filtro = st.sidebar.selectbox('Graph Type',
                                       options=['Map of Incidents 2018-2020', 
                                                'Count Per Type of Crimes 2018-2020',
                                                'Incidences Per Day by Year',
                                                'Resolution Distribution'])

#Mapa
if filtro == 'Map of Incidents 2018-2020':
    dfLat = df['Latitude'].dropna(axis = 0, how = 'any')
    dfLon = df['Longitude'].dropna(axis = 0, how = 'any')

    mapapol = pd.DataFrame()
    a = dfLat
    b = dfLon
    mapapol['lat'] = a
    mapapol['lon'] = b
    st.map(mapapol)
    
    
chart_data_bars = pd.DataFrame()
cantidades = [157471,48222,21101,11269,8156,6002]
tipocrimen = ["Initial", "Coplogic Initial", "Initial Supplement", "Vehicle Initial", "Vehicle Supplement", "Coplogic Supplement"]
chart_data_bars['Count'] = cantidades
chart_data_bars['Crime'] = tipocrimen
if filtro == 'Count Per Type of Crimes 2018-2020':
#Gráfica de tipo de crimenes
    fig1 = px.bar(chart_data_bars, x = 'Crime', y = 'Count')
    st.plotly_chart(fig1)


#Gráfica de lineas por día de la semana
def sorter(column):
    reorder = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
      
    ]
    cat = pd.Categorical(column, categories=reorder, ordered=True)
    return pd.Series(cat)
cont2018 = cont2018.sort_index(key=sorter)
cont2019 = cont2019.sort_index(key=sorter)
cont2020 = cont2020.sort_index(key=sorter)
if filtro == 'Incidences Per Day by Year':
    fig = px.line(cont2018, x=cont2018.index, y=cont2018.values)
    fig.update_layout(title='Amount of Incidences Per Day of the Week in 2018',
                      xaxis_title='Day of the Week',yaxis_title='Count of Incidences')
    st.plotly_chart(fig)
    
    fig = px.line(cont2019, x=cont2019.index, y=cont2019.values)
    fig.update_layout(title='Amount of Incidences Per Day of the Week in 2019',
                      xaxis_title='Day of the Week',yaxis_title='Count of Incidences')
    st.plotly_chart(fig)
    
    fig = px.line(cont2020, x=cont2020.index, y=cont2020.values)
    fig.update_layout(title='Amount of Incidences Per Day of the Week in 2020',
                      xaxis_title='Day of the Week',yaxis_title='Count of Incidences')
    st.plotly_chart(fig)

if filtro == 'Resolution Distribution':
#Gráfica de pastel de tipo de resolution
    fig = px.pie(dfpastel, values=dfpastel.values, names=dfpastel.index, title='Resolution Total Distribution')
    st.plotly_chart(fig)
