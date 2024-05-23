import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from datetime import date, timedelta

## F U N C T I O N S ##
def update_units():
    units.to_csv("dgo_units.csv")

def get_active_units():
    active_units = units[units["Status"]=="active"].iloc[:]["Grafana ID"]
    return active_units

## Streamlit headings and formatting
st.sidebar.header('DGO Tracking Tool')

tab1, tab2, tab3 = st.tabs(["DGO Data", "Test Tracker", "Unit Info"])
# import csv containing unit info
units = pd.read_csv("./dgo_units.csv")

# sidebar data entry
with st.sidebar:
    st.write(date.today().strftime("%B %d, %Y"))
    st.subheader("Daily Logger")
    st.selectbox("Unit:", get_active_units(), None)

    # st.number_input("")
with tab2:
    tests = pd.DataFrame
# if adding new unit:
with tab3:
    st.data_editor(
        units, 
        num_rows="dynamic",
        # on_change = update_units,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                default="inactive",
                options=[
                    "active",
                    "inactive",
                    "decommissioned",
                ],

            )
        }
    )

    add_unit = st.checkbox("New Unit")
    if add_unit:
        with st.form("add_unit", clear_on_submit=True):
            st.write("Add a new unit")

            unit_sn = st.text_input("Serial Number")
            grafana_id = st.text_input("Grafana ID")
            tailscale_id = st.text_input("Tailscale ID")
            
            submitted = st.form_submit_button("Submit")

            if submitted:
                new_unit = pd.DataFrame({"Grafana ID": [grafana_id], "Serial Number": [unit_sn], "Tailscale ID": [tailscale_id]})

                # units.loc[len(units)] = new_unit
                units = pd.concat([units, new_unit], ignore_index=True)
                update_units()
                add_unit = False

                
                # append unit info to csv


# import file containing unit ids and their data
# be able to append units to data
# open csv and append inputs
# 

# spit out chart?
# scrape data from grafana?