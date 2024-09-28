"""
data from https://ourworldindata.org/grapher/primary-sub-energy-source
should automate downloading the csv - for the moment stored manually

"""
import pandas as pd 
import plotly.express as px
import streamlit as st


@st.cache_data
def load_data():

    df=pd.read_csv('../Files/primary-sub-energy-source.csv')
    df.rename(columns=lambda s: s.replace(" consumption - TWh", ""), inplace=True)
    df.rename(columns={'Other renewables (including geothermal and biomass) - TWh':'Other renewables'}, inplace=True)
    df.iloc[:,3:]=df.iloc[:,3:].astype(float)
    lastYear=df['Year'].max()
    dfLast=df[df['Year']==lastYear]
    return dfLast, lastYear

dfLast,lastYear = load_data()

dfWorldLast = dfLast[dfLast['Entity']=='World']
dfWorldLast = dfWorldLast.T.iloc[3:]
dfWorldLast.columns=['Energy source']
dfWorldLast.iloc[0]=dfWorldLast.iloc[0].astype(float)
total = dfWorldLast.sum().values[0]
# print(total)
st.title('Energy statistics, from Our World in Data')
st.write("static data from https://ourworldindata.org/grapher/primary-sub-energy-source")
title = f'{lastYear} World energy consumption by source, TWh <br>Total: {total:,.0f} TWh'
fig = px.pie(dfWorldLast,values='Energy source',names=dfWorldLast.index,title=title)
# fig.update_traces(hoverinfo='percent+value')
fig.update_traces(texttemplate = "%{label}: %{value:,.2s} <br>(%{percent})",textposition = "inside")
fig.update_layout(height=1000,width=1000)
st.plotly_chart(fig, use_container_width=True)
