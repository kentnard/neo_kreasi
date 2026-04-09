import streamlit as st
import sqlite3
import pandas as pd

from utils.sql_utils import get_all_furnitures, get_furniture_details, add_new_furniture, get_all_materials, add_new_material_to_furniture, edit_furniture
from utils.streamlit_utils import confirm_delete_furniture_dialog
from utils.python_utils import format_amount

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.rerun()

st.title("Furniture Management")

tab1, tab2, tab3, tab4 = st.tabs(["View Furnitures", "Add Furnitures", "Edit Furnitures", "Delete Furnitures"])

with tab1:
    # View Furniture
    st.subheader("Current furnitures in the database")
    df = get_all_furnitures()
    df.rename(columns={"FID": "ID"}, inplace=True)
    st.dataframe(df.style.format({
        "Total Purchase Price": lambda x: f"{int(x):,}".replace(",", ".")
    }), hide_index=True)

    furniture_id_show = st.selectbox("Select a furniture to see its details",
                             options=df["ID"].tolist(),
                            format_func=lambda fid: df.loc[df["ID"] == fid, "Furniture Name"].values[0],
                            key="furniture_detail_selectbox")
    
    df_details = get_furniture_details(furniture_id_show)
    st.dataframe(df_details.style.format({
        "Purchase Price": lambda x: f"{int(x):,}".replace(",", "."),
        "Amount": format_amount,
        "Cost": lambda x: f"{int(x):,}".replace(",", "."),
    }), hide_index=True)

    current_furniture_name = df.loc[df["ID"] == furniture_id_show, "Furniture Name"].values[0]
    st.markdown(
    f"<p style='font-size:25px; font-weight:bold;'>"
    f"Total cost: Rp{df_details['Cost'].sum():,.0f}".replace(",", ".") +
    "</p>",
    unsafe_allow_html=True
)

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
    st.dataframe(df.style.format({
        "Total Purchase Price": lambda x: f"{int(x):,}".replace(",", ".")
    }), hide_index=True)

    selected_furniture = st.selectbox("Select a furniture to add materials to",
                                      df["ID"].tolist(),
                                      index=None,
                                      placeholder="Select  a furniture",
                                      format_func=lambda fid: df.loc[df["ID"] == fid, "Furniture Name"].values[0],
                                      key="add_material_furniture_selectbox")
    
    # Show the current materials of the chosen furniture
    df_details = get_furniture_details(selected_furniture)
    if len(df_details) > 0 :
        st.dataframe(df_details.style.format({
            "Purchase Price": lambda x: f"{int(x):,}".replace(",", "."),
            "Amount": format_amount,
            "Cost": lambda x: f"{int(x):,}".replace(",", "."),
        }), hide_index=True)

    # Show all materials
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
    # Edit furniture (name & desc only)
    st.subheader("Current furniture in the database")
    df = get_all_furnitures()
    df.rename(columns={"FID": "ID"}, inplace=True)
    st.dataframe(df.style.format({
        "Total Purchase Price": lambda x: f"{int(x):,}".replace(",", ".")
    }), hide_index=True)

    st.subheader("Select a furniture to edit and fill in the new values.")
    furniture_id_update = st.selectbox("Select furniture to update",
                                options=df["ID"].tolist(),
                                index=None,
                                format_func=lambda fid: df.loc[df["ID"] == fid, "Furniture Name"].values[0],
                                key="edit_furniture_selectbox"
                                )
    if furniture_id_update is None : 
        st.info("Please select a furniture to edit.")
    else :
        # Current values of the selected furniture
        row = df.loc[df["ID"] == furniture_id_update].iloc[0]
        current_furniture_name = row["Furniture Name"]
        current_description = row["Description"]

        st.warning("Leave a field BLANK if you do not wish to change it. If you want to remove the description, just input a single hyphen (-).")

        st.write(current_furniture_name, current_description)
        new_furniture_name = st.text_input("New Furniture Name",
                                          help="Only insert furniture name here!",
                                          key="new_furniture_name_edit")
        new_description = st.text_area("New Description",
                                      help="Insert furniture description here!", key="new_furniture_description_edit")

        if st.button("Update furniture"):
            if new_furniture_name == "" and new_description == "":
                st.error("Please fill in AT LEAST ONE field.")
            else: 
                new_furniture_name = new_furniture_name or current_furniture_name
                if new_description == "-":
                    new_description = ""
                elif new_description == "":
                    new_description = current_description
                edit_furniture(furniture_id_update, new_furniture_name, new_description)

    # This is where the user can edit the materials in a single furniture 
    st.write("Under consturction")

with tab4:
    # Delete the furniture
    st.subheader("Current furniture in the database")
    df = get_all_furnitures()
    df.rename(columns={"FID": "ID"}, inplace=True)
    st.dataframe(df.style.format({
        "Total Purchase Price": lambda x: f"{int(x):,}".replace(",", ".")
    }), hide_index=True)

    st.subheader("Delete existing furnitures in the database")
    st.warning("**Warning:** Deleting a furniture is irreversible. Please consider EDITING it before deleting it.")

    furniture_id_to_delete = st.selectbox("Select furniture to delete",
                                 options=df["ID"].tolist(),
                                index=None,
                                placeholder="Select a furniture to delete",
                                format_func=lambda fid: df.loc[df["ID"] == fid, "Furniture Name"].values[0],
                                key="delete_furniture_selectbox"
                                )
    if st.button("Delete furniture"):
        confirm_delete_furniture_dialog(furniture_id_to_delete)

    # The user should be able to delete materials from a furniture here
    st.write("Under consturction")