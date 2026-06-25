import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('leaves.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leaves 
                 (username TEXT, leave_type TEXT, from_date TEXT, to_date TEXT, reason TEXT, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- Your Existing UI Logic ---
# [Keep your login and sidebar logic as is]

# --- Replacing "Submit" logic with Database insert ---
if st.button("Submit Request", type="primary"):
    # ... [Keep your validation logic here] ...
    conn = sqlite3.connect('leaves.db')
    c = conn.cursor()
    c.execute("INSERT INTO leaves VALUES (?,?,?,?,?,?)", 
              (st.session_state.username, leave_type, str(from_date), str(to_date), reason, "Pending"))
    conn.commit()
    conn.close()
    st.success("✅ Saved to Database!")

# --- Replacing "History" tab with Pandas + Database ---
with tab2:
    conn = sqlite3.connect('leaves.db')
    df = pd.read_sql(f"SELECT * FROM leaves WHERE username='{st.session_state.username}'", conn)
    conn.close()
    st.table(df) # Shows data nicely using Pandas
