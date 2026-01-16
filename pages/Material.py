import streamlit as st
import sqlite3
import pandas as pd

from utils.db_helper import get_db_connection
from utils.sql_utils import get_all_materials, add_new_material, edit_material
from utils.streamlit_utils import confirm_delete_material_dialog

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.rerun()

st.title("Material Management")

tab1, tab2, tab3, tab4 = st.tabs(["View Materials", "Add Material", "Edit Material", "Delete Material"])

# Read all materials from the database
with tab1:
    st.subheader("Current materials in the database")
    df = get_all_materials()
    df.rename(columns={"MID": "ID"}, inplace=True)
    st.dataframe(df, hide_index=True)

# Add new materials to the database
with tab2:
    st.subheader("Fill in the form below to add a new material.")
    new_material_name = st.text_input("Material Name", help="Only insert material name here!", key="new_name_create")
    new_material_unit = st.text_input("Unit", help="Only insert material unit here!", key="new_unit_create")
    new_price = st.number_input("Purchase price", min_value=0, placeholder=10000, step=1, help="Only insert material purchase price here!", key="new_price_create")

    if st.button("Add material"):
        if new_material_name and new_material_unit and new_price:
            add_new_material(new_material_name, new_material_unit, new_price)

        else:
            st.error("Please fill in ALL fields.")
    

# Add new materials to the database
with tab3:
    st.subheader("Current materials in the database")
    df = get_all_materials()
    df.rename(columns={"MID": "ID"}, inplace=True)
    st.dataframe(df, hide_index=True)

    st.subheader("Select a material to edit and fill in the new values.")
    id_to_update = st.selectbox("Select material to edit",
                                options=df["ID"].tolist(),
                                index=None,
                                format_func=lambda mid: df.loc[df["ID"] == mid, "Material Name"].values[0],
                                key= "edit_selectbox"
                                )
    
    # Current values of the selected material
    row = df.loc[df["ID"] == id_to_update].iloc[0]
    current_name = row["Material Name"]
    current_unit = row["Unit"]
    current_price = row["Purchase Price"]
    
    # User input of new values 
    st.warning("Leave a field BLANK if you do not wish to change it.")
    new_material_name2 = st.text_input("Material Name",
                                       help="Only insert material name here!",
                                       key="new_name_edit")
    new_material_unit2 = st.text_input("Unit",
                                       help="Only insert material unit here!",
                                       key="new_unit_edit")
    new_price2 = st.number_input("Purchase price",
                                 min_value=0,
                                 placeholder=10000,
                                 step=1,
                                 help="Only insert material purchase price here!",
                                 key="new_price_edit")

    # Check if it's empty, if yes, assign the current value
    if st.button("Update material") :
        if new_material_name2 == "" and new_material_unit2 == "" and new_price2 == 0 :
            st.error("Please fill in AT LEAST ONE field to update.")
        else :
            new_material_name2 = new_material_name2 or current_name
            new_material_unit2 = new_material_unit2 or current_unit
            new_price2 = new_price2 if new_price2 not in (0, None) else current_price

            edit_material(id_to_update, new_material_name2, new_material_unit2, new_price2)

with tab4:
    st.subheader("Current materials in the database")
    df = get_all_materials()
    df.rename(columns={"MID": "ID"}, inplace=True)
    st.dataframe(df, hide_index=True)

    st.subheader("Select a material to delete.")
    st.warning("**Warning:** Deleting a material is irreversible and may affect related furniture. Please consider EDITING it before deleting it.")

    id_to_delete = st.selectbox("Select material to delete",
                             options=df["ID"].tolist(),
                            format_func=lambda mid: df.loc[df["ID"] == mid, "Material Name"].values[0], key= "delete_selectbox"
                            )
    if st.button("Delete material"):
        confirm_delete_material_dialog(id_to_delete)