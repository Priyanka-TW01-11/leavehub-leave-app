import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# --- Setup ---
st.set_page_config(page_title="LeafFlow 🌿", page_icon="🌿", layout="centered")

def init_db():
    conn = sqlite3.connect('leaves.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leaves 
                 (username TEXT, leave_type TEXT, from_date TEXT, to_date TEXT, reason TEXT, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- Auth ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
users = {"rahul": "1234", "priya": "1234"}

# --- UI ---
st.title("🌿 LeafFlow")

if not st.session_state.logged_in:
    st.subheader("🔑 Login")
    user = st.text_input("Username").strip().lower()
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user in users and users[user] == pwd:
            st.session_state.update({'logged_in': True, 'username': user})
            st.rerun()
        else: st.error("Invalid credentials")
else:
    st.success(f"Logged in as {st.session_state.username.capitalize()}")
    if st.button("Logout"):
        st.session_state.update({'logged_in': False, 'username': None})
        st.rerun()

    # DEFINING TABS AT THE TOP LEVEL (This prevents the NameError)
    tab1, tab2, tab3 = st.tabs(["📝 Apply", "📋 History", "🗓️ Holidays"])

    with tab1:
        st.subheader("New Request")
        l_type = st.selectbox("Type", ["Casual", "Sick", "Privilege"])
        f_date = st.date_input("From")
        t_date = st.date_input("To")
        reason = st.text_area("Reason")
        if st.button("Submit"):
            if f_date.weekday() >= 5 or t_date.weekday() >= 5:
                st.error("No weekends!")
            else:
                conn = sqlite3.connect('leaves.db')
                c = conn.cursor()
                c.execute("INSERT INTO leaves VALUES (?,?,?,?,?,?)", 
                          (st.session_state.username, l_type, str(f_date), str(t_date), reason, "Pending"))
                conn.commit()
                conn.close()
                st.success("Submitted!")

    with tab2:
        st.subheader("History")
        conn = sqlite3.connect('leaves.db')
        df = pd.read_sql(f"SELECT * FROM leaves WHERE username='{st.session_state.username}'", conn)
        conn.close()
        st.table(df)

    with tab3:
        st.write("• 2026-01-26: Republic Day\n• 2026-08-15: Independence Day")
        
