import streamlit as st
import sqlite3
import pandas as pd

from utils.sql_utils import get_all_furnitures, get_furniture_details

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.rerun()

st.title("Furniture Management")

tab1, tab2, tab3, tab4 = st.tabs(["View Furnitures", "Add Furnitures", "Edit Furnitures", "Delete Furnitures"])

with tab1:
    st.subheader("Current furnitures in the database")
    df = get_all_furnitures()
    df.rename(columns={"FID": "ID"}, inplace=True)
    st.dataframe(df, hide_index=True)

    furniture_id_show = st.selectbox("Select a furniture to see its details",
                             options=df["ID"].tolist(),
                            format_func=lambda fid: df.loc[df["ID"] == fid, "Furniture Name"].values[0],
                            key="furniture_detail_selectbox")
    
    df_details = get_furniture_details(furniture_id_show)
    st.dataframe(df_details, hide_index=True)

    df_details["Cost"] = df_details["Amount"] * df_details["Purchase Price"]

    current_furniture_name = df.loc[df["ID"] == furniture_id_show, "Furniture Name"].values[0]
    st.write(f"**Total cost:** : Rp{df_details['Cost'].sum():,.0f}".replace(",", "."))



with tab2:
    st.subheader("Fill in the form below to add a new furniture.")
    st.write("Under consturction")

with tab3:
    st.subheader("Edit existing furnitures in the database")
    st.write("Under consturction")

with tab4:
    st.subheader("Delete existing furnitures in the database")
    st.write("Under consturction")