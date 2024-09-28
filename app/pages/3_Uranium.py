"""
data from https://ourworldindata.org/grapher/primary-sub-energy-source
should automate downloading the csv - for the moment stored manually

"""
#%%
import pandas as pd 
import plotly.express as px
import streamlit as st


def load_data():
        dfs=pd.read_html("https://world-nuclear.org/information-library/facts-and-figures/uranium-production-figures.aspx")

        df = dfs[0].copy()
        df.set_index('Country',inplace=True)
        df.replace('%','',regex=True,inplace=True)
        df=df.astype(float)
        df.iloc[-1]*=0.01
        return df

df = load_data()

fig1=px.bar(df.loc['Total world'].T,
        title='Annual Uranium production').update_layout(xaxis_title='Year',yaxis_title='Tonnes')

dfLast = df.iloc[:-3,-1]

fig2=px.pie(dfLast,values=dfLast.values,names=dfLast.index,title='Uranium production by country',
            height=800,width=800)


st.title('Uranium production')
st.write("data live from https://world-nuclear.org/information-library/facts-and-figures/uranium-production-figures")
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
