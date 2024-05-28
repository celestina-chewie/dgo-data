import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

fig = go.Figure()

def plot_data(x,y,name):
    fig.add_trace(go.Scatter(x=x,y=y,name=name,line_shape='linear'))

uploaded_data = st.file_uploader("Upload csvs: ", accept_multiple_files=True)
for uploaded_file in uploaded_data:
    data_file = uploaded_file.read()
#pick which variables to display
    st.selectbox("Select Variables", data_file[1])
#have average data store/on hand maybe on own tab?