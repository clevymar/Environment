import streamlit as st

from common import dirFiles

st.set_page_config(layout="wide")

st.title("Environment data explorer")
st.write('Developped by CLM, first release Sep 2024')

st.write(dirFiles)