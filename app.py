import streamlit as st
from datetime import date

# Page Configuration
st.set_page_config(
    page_title="LeafFlow 🌿",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 LeafFlow")
st.caption("Employee Leave Management System")

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'leaves' not in st.session_state:
    st.session_state.leaves = []

# Hardcoded Users for Demo
users = {"rahul": "1234", "priya": "1234"}

# ====================== LOGIN SCREEN ======================
if not st.session_state.logged_in:
    st.subheader("🔑 Login to LeafFlow")
    
    username = st.text_input("Username", placeholder="rahul or priya").strip().lower()
    password = st.text_input("Password", type="password", value="1234")
    
    if st.button("Login", use_container_width=True):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Welcome, {username.capitalize()}!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Try: **rahul** or **priya** (Password: 1234)")
else:
    # ====================== MAIN APP ======================
    st.success(f"👋 Logged in as {st.session_state.username.capitalize()}")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    # Leave Balance
    st.subheader("📊 Your Leave Balance")
    st.markdown("""
    • **Casual Leave**: 12 days  
    • **Sick Leave**: 10 days  
    • **Privilege Leave**: 15 days
    """)

    tab1, tab2, tab3 = st.tabs(["📝 Apply Leave", "📋 History", "🗓️ 2026 Holidays"])

    with tab1:
        st.subheader("New Leave Request")
        leave_type = st.selectbox("Leave Type", 
            ["Casual Leave", "Sick Leave", "Privilege Leave", "Maternity Leave"])
        
        col1, col2 = st.columns(2)
        with col1:
            from_date = st.date_input("From Date", value=date(2026, 1, 20))
        with col2:
            to_date = st.date_input("To Date", value=date(2026, 1, 22))
        
        reason = st.text_area("Reason", placeholder="Family function / Medical appointment...")
        
        if st.button("Submit Request", type="primary", use_container_width=True):
            if from_date.weekday() >= 5 or to_date.weekday() >= 5:
                st.error("❌ Weekend leaves are not allowed!")
            elif from_date > to_date:
                st.error("❌ From date cannot be after To date")
            else:
                st.session_state.leaves.insert(0, {
                    "Date": str(from_date),
                    "Type": leave_type,
                    "Status": "Pending",
                    "Reason": reason if reason else "No reason provided"
                })
                st.success("✅ Leave request submitted successfully!")
                st.balloons()

    with tab2:
        st.subheader("Leave History")
        if st.session_state.leaves:
            for leave in st.session_state.leaves:
                st.write(f"**{leave['Date']}** — {leave['Type']}")
                st.write(f"Status: **{leave['Status']}**")
                st.write(f"Reason: {leave['Reason']}")
                st.divider()
        else:
            st.info("No leave requests yet. Apply one from the first tab.")

    with tab3:
        st.subheader("2026 Public Holidays")
        holidays = [
            "2026-01-01 - New Year's Day",
            "2026-01-26 - Republic Day",
            "2026-03-04 - Holi",
            "2026-03-21 - Eid-ul-Fitr",
            "2026-04-03 - Good Friday",
            "2026-08-15 - Independence Day",
            "2026-10-02 - Gandhi Jayanti",
            "2026-12-25 - Christmas"
        ]
        for h in holidays:
            st.markdown(f"• **{h}**")

st.caption("Made with ❤️ for Priyanka")
