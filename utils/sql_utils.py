import streamlit as st
import pandas as pd
import sqlite3

from utils.db_helper import get_db_connection

conn, cursor = get_db_connection()

def get_all_materials() -> pd.DataFrame:
    """
    Get all materials from tha table "materials"

    Returns:
        pd.DataFrame: DataFrame containing all materials
    """
    cursor.execute("SELECT * FROM materials")
    conn.commit()

    all_materials = cursor.fetchall()

    return pd.DataFrame(all_materials, columns=["MID", "Material Name", "Unit", "Purchase Price"])

def add_new_material(name : str, unit : str, purchasePrice : float) -> None:
    """
    Add a new material to the table "materials". This assumes that the name, unit and purchasePrice are syntactically correct. The uniqueness test will be handled here.

    Returns:
        None
    """
    try : 
        cursor.execute(
            "INSERT INTO materials (name, unit, purchasePrice) VALUES (?, ?, ?)",
            (name, unit, purchasePrice),
        )
        conn.commit()
        st.success(f"Material '{name}' added successfully!")
    except sqlite3.IntegrityError as e:
        st.error(f"Error adding material: {e}. Please ensure the material name is unique.")
    except Exception as e:
        st.error(f"Error adding material: {e}. Please contact admin.")

def edit_material(mid : int, name : str, unit : str, purchasePrice : float) -> None:
    """
    Edit an existing material in the table "materials", given the MID, the name, unit and purchasePrice. This assumes that the name, unit and purchasePrice are syntactically correct. The uniqueness test will be handled here.

    Returns:
        None
    """
    try:
        cursor.execute(
            "UPDATE materials SET name=?, unit=?, purchasePrice=? WHERE MID=?",
            (name, unit, purchasePrice, mid)
        )
        conn.commit()
        st.success(f"Material with ID {mid} updated successfully!")
    except sqlite3.IntegrityError as e:
        st.error(f"Error editing material: {e}. Please ensure the material name has not existed yet.")
    except Exception as e:
        st.error(f"Error editing material: {e}. Please contact admin.")

def delete_material(mid : int) -> None:
    """
    Delete an existing material in the table "materials", given the MID.

    Returns:
        None
    """
    try:
        cursor.execute(
            "DELETE FROM materials WHERE MID=?",
            (mid,)
        )
        conn.commit()
        st.success(f"Material with ID {mid} deleted successfully!")
    except Exception as e:
        st.error(f"Error deleting material: {e}. Please contact admin.")