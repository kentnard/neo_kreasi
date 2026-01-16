import streamlit as st
import sqlite3
import pandas as pd

from utils.sql_utils import get_all_furnitures, get_furniture_details, add_new_furniture, get_all_materials, add_new_material_to_furniture

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
    # Only add new furniture
    st.subheader("Fill in the form below to add a new furniture")
    new_furniture_name = st.text_input("Furniture Name",
                                       help="Only insert furniture name here!",
                                       key="new_furniture_name_create")
    new_furniture_description = st.text_area("Description",
                                             help="Insert furniture description here!", key="new_furniture_description_create")

    if st.button("Add furniture"):
        if new_furniture_name:
            add_new_furniture(new_furniture_name, new_furniture_description)
            
        else:
            st.error("Please fill in ALL required fields.")

    # Here the user can add materials to an existing furniture
    st.subheader("Fill in the form below to add materials to a (an already existing) furniture")
    df = get_all_furnitures()
    df.rename(columns={"FID": "ID"}, inplace=True)
    st.dataframe(df, hide_index=True)

    selected_furniture = st.selectbox("Select a furniture to add materials to",
                                      df["ID"].tolist(),
                                      index=None,
                                      placeholder="Select  a furniture",
                                      format_func=lambda fid: df.loc[df["ID"] == fid, "Furniture Name"].values[0],
                                      key="add_material_furniture_selectbox")

    df_all_materials = get_all_materials()
    df_all_materials.rename(columns={"MID": "ID"}, inplace=True)

    selected_material = st.selectbox("Select a material to add to the furniture",
                                     df_all_materials["ID"].tolist(),
                                     index=None,
                                     placeholder="Select a material",
                                     format_func=lambda mid: df_all_materials.loc[df_all_materials["ID"] == mid, "Material Name"].values[0],
                                     key="add_material_to_furniture_selectbox")
    chosen_amount = st.number_input("Amount of material",
                                    min_value=0.0,
                                    format="%.2f",
                                    help="Insert the amount of material to add to the furniture here!",
                                    key="add_material_amount_input")

    if st.button("Add material to furniture"):
        if selected_furniture and selected_material and chosen_amount not in(0, None):
            add_new_material_to_furniture(selected_furniture, selected_material, chosen_amount)
        else: 
            st.error("Please fill in ALL fields.")
            
with tab3:
    st.subheader("Edit existing furnitures in the database")
    st.write("Under consturction")

with tab4:
    st.subheader("Delete existing furnitures in the database")
    st.write("Under consturction")