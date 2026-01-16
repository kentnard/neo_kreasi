import streamlit as st
import sqlite3

# Create persisent DB connection
DB_PATH = "database/neo_kreasi_db.db"
def get_db_connection():
    if "conn" not in st.session_state:
        try :
            st.session_state["conn"] = sqlite3.connect(DB_PATH, check_same_thread=False)
            st.session_state["cursor"] = st.session_state["conn"].cursor()
            st.session_state.db_initialized = True
            st.success("Database connection established!")
            return st.session_state["conn"], st.session_state["cursor"]
        
        except Exception as e:
            st.error(f"Failed to connect to database: {e}. Please contact admin.")
            st.session_state.db_initialized = False