import streamlit as st
from datetime import date

# Page Configuration
st.set_page_config(page_title="LeafFlow 🌿", page_icon="🌿", layout="centered")

st.title("🌿 LeafFlow")
st.caption("Employee Leave Management System")

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'leaves' not in st.session_state:
    st.session_state.leaves = []

# Hardcoded Users
users = {"rahul": "1234", "priya": "1234"}

# Login Logic
if not st.session_state.logged_in:
    st.subheader("🔑 Login to LeafFlow")
    username = st.text_input("Username").strip().lower()
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid credentials.")
else:
    st.success(f"Logged in as {st.session_state.username}")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["📝 Apply", "📋 History", "🗓️ Holidays"])
    
    with tab1:
        leave_type = st.selectbox("Leave Type", ["Casual", "Sick", "Privilege"])
        f_date = st.date_input("From Date")
        t_date = st.date_input("To Date")
        reason = st.text_area("Reason")
        if st.button("Submit"):
            st.session_state.leaves.append({"Date": f_date, "Type": leave_type})
            st.success("Submitted!")

    with tab2:
        st.write(st.session_state.leaves)

    with tab3:
        st.write("2026 Public Holidays")
