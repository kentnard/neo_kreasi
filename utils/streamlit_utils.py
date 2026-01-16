import streamlit as st

from utils.sql_utils import delete_material

@st.dialog("Confirm Deletion")
def confirm_delete_material_dialog(id_to_delete: int) -> None:
    st.write("Are you sure you want to delete this material? This action cannot be undone.")
    if st.button("Yes, delete it"):
        delete_material(id_to_delete)