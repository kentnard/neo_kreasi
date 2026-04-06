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
    try :
        cursor.execute("SELECT * FROM materials")
        conn.commit()

        all_materials = cursor.fetchall()

        return pd.DataFrame(all_materials, columns=["MID", "Material Name", "Unit", "Purchase Price"])

    except Exception as e:
        st.error(f"Error fetching all materials: {e}. Please contact admin.")

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

def get_all_furnitures() -> pd.DataFrame:
    """
    Get all furnitures from the table "furnitures"

    Returns:
        pd.DataFrame: DataFrame containing all furnitures
    """
    try : 
        cursor.execute("""SELECT f.fid, 
                       f.name,
                       f.description,
                       coalesce(SUM(fm.amount*m.purchasePrice), 0) AS total_price
                        FROM furnitures f
                        LEFT JOIN furniture_materials fm
                            ON f.fid = fm.fid
                        LEFT JOIN materials m
                            ON fm.mid = m.mid
                        GROUP BY f.fid, f.name, f.description""")
        conn.commit()

        all_furnitures = cursor.fetchall()

        return pd.DataFrame(all_furnitures, columns=["FID", "Furniture Name", "Description", "Total Purchase Price"])

    except Exception as e:
        st.error(f"Error fetching all furnitures: {e}. Please contact admin.")

def get_furniture_details(fid : int) -> pd.DataFrame:
    """
    Get the details of a furniture from the table "furniture_materials", given the FID.

    Returns:
        pd.DataFrame: DataFrame containing the furniture details
    """
    try :
        cursor.execute("""SELECT f.name, m.name, fm.amount, m.unit, m.purchasePrice
                       FROM furnitures f
                       JOIN furniture_materials fm ON f.fid = fm.fid
                       JOIN materials m on fm.mid = m.mid
                       WHERE f.fid=?""", 
                       (fid,))
        conn.commit()

        furniture_details = cursor.fetchall()

        return pd.DataFrame(furniture_details, columns=["Furniture Name", "Material Name", "Amount", "Unit", "Purchase Price"])
    
    except Exception as e:
        st.error(f"Error fetching furniture details: {e}. Please contact admin.")

def add_new_furniture(name : str, description : str) -> None:
    """
    Add a new furniture to the table "furnitures". This assumes that the name and description are syntactically correct. The uniqueness test will be handled here. The description can be empty.

    Returns:
        None
    """
    try : 
        cursor.execute(
            "INSERT INTO furnitures (name, description) VALUES (?, ?)",
            (name, description),
        )
        conn.commit()
        st.success(f"Furniture '{name}' added successfully!")
    except sqlite3.IntegrityError as e:
        st.error(f"Error adding furniture: {e}. Please ensure the furniture name is unique.")
    except Exception as e:
        st.error(f"Error adding furniture: {e}. Please contact admin.")

def add_new_material_to_furniture(fid : int, mid : int, amount : float) -> None:
    """
    Add a new material to a furniture in the table "furniture_materials". This assumes that the fid, mid and amount are syntactically correct. The uniqueness test will be handled here.

    Returns:
        None
    """
    try : 
        cursor.execute(
            "INSERT INTO furniture_materials (fid, mid, amount) VALUES (?, ?, ?)",
            (fid, mid, amount),
        )
        conn.commit()
        st.success(f"Material with ID '{mid}' added to furniture with ID '{fid}' successfully!")
    except sqlite3.IntegrityError as e:
        st.error(f"Error adding material to furniture: {e}. Please ensure the material is not already added to the furniture.")
    except Exception as e:
        st.error(f"Error adding material to furniture: {e}. Please contact admin.")

def edit_furniture(fid : int, name : str, description : str) -> None:
    """
    Edit an existing furniture in the table "furnitures", given the FID, the name and description. This assumes that the name and description are syntactically correct. The uniqueness test will be handled here.

    Returns:
        None
    """
    try:
        cursor.execute(
            "UPDATE furnitures SET name=?, description=? WHERE FID=?",
            (name, description, fid)
        )
        conn.commit()
        st.success(f"Furniture with ID {fid} updated successfully!")
    except sqlite3.IntegrityError as e:
        st.error(f"Error editing furniture: {e}. Please ensure the furniture name has not existed yet.")
    except Exception as e:
        st.error(f"Error editing furniture: {e}. Please contact admin.")

def delete_furniture(fid : int) -> None:
    """
    Delete an existing furniture in the table "furnitures", given the FID.

    Returns:
        None
    """
    try:
        cursor.execute(
            "DELETE FROM furnitures WHERE FID=?",
            (fid,)
        )
        conn.commit()
        st.success(f"Furniture with ID {fid} deleted successfully!")
    except Exception as e:
        st.error(f"Error deleting furniture: {e}. Please contact admin.")