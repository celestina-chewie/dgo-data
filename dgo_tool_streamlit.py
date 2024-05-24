import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from datetime import date, timedelta

## F U N C T I O N S ##
def update_units(units):
    units.to_csv("dgo_units.csv", index=False)

def get_active_units():
    active_units = units[units["Status"]=="active"].iloc[:]["Grafana ID"]
    return active_units

## Streamlit headings and formatting
st.sidebar.header('DGO Algo Tracking')

tab1, tab2, tab3 = st.tabs(["DGO Data", "Recipes", "Unit Info"])
# import csv containing unit info
units = pd.read_csv("./dgo_units.csv")

dgo_data = pd.read_csv("./daily_dgo_data.csv")
with tab2:
    tests = pd.DataFrame
# if adding new unit:
with tab3:
    # if 'units' not in st.session_state:
    #     st.session_state.units = pd.read_csv("./dgo_units.csv")

    editable_units = st.data_editor(
        units, 
        num_rows="dynamic",
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

    if editable_units.equals(units):
        st.session_state["units_updated"] = False
    else:
        st.session_state["units_updated"] = True
        update_units(editable_units)


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
                update_units(units)
                add_unit = False

                
                # append unit info to csv

# sidebar data entry
with st.sidebar:
    st.write(date.today().strftime("%B %d, %Y"))
    st.subheader("Daily Logger")
    pick_unit = st.selectbox("Unit:", get_active_units(), None)
    if pick_unit:
        # st.selectbox("Food Input")
        with st.form("Data:", clear_on_submit=True):
            recipes = pd.read_csv("./recipes.csv")
            #Show input variables
            # inputs = {'pre_feed_mass':[], 'added_dry':[], 'added_wet':[], 'post_feed_mass':[], 'mc':[]}
            pre_feed_mass = st.number_input("Pre-Feeding Mass (kg):")
            added_dry = st.number_input("Added Dry FG Mass (kg):")
            added_wet = st.selectbox(
                "Added Wet Food Mass (kg):", 
                recipes["mass"], 
                placeholder="Select one",
            )
            post_feed_mass = st.number_input("Post-Feeding Mass (kg):")
            mc = st.number_input("Moisture Content:")
            #calculate additional metrics
            dry_mc = 0.1
            wet_mc = 0.77
            unit_tare_weight = units[units["Grafana ID"]==pick_unit].iloc[0]["Tare Weight"]

            # prev_mc = dgo_data["Moisture Content"].where(dgo_data["Unit"].equals(pick_unit) and dgo_data["Date"].equals(date.today()-timedelta(days=1)))
            with tab1:
                st.dataframe(dgo_data)
            
            prev_mc = dgo_data[dgo_data["Unit"] == pick_unit].iloc[:][dgo_data["Date"] == str(date.today()-timedelta(days=1))].iloc[0]["Moisture Content"]

            print(dry_mc)
            post_feed_food_mass = post_feed_mass - unit_tare_weight
            post_feed_wet_mc = (added_dry*dry_mc + added_wet*wet_mc + (prev_mc/100 * (pre_feed_mass-unit_tare_weight)) / post_feed_food_mass)

        
            #Post Feed Wet  MC
            st.write("Post Feed Wet MC:"+str(post_feed_wet_mc))

            #Post Feed Food Mass (kg)
            st.write("Post Feed Food Mass (kg):"+str(post_feed_food_mass))

            submitted = st.form_submit_button("Submit")
            if submitted: 
                new_data_point = pd.DataFrame({"Date":[date.today()],"Unit":[pick_unit]})


    # st.number_input("")
# import file containing unit ids and their data
# be able to append units to data
# open csv and append inputs
# 

# spit out chart?
# scrape data from grafana?