import streamlit as st
import sys
import os
from database.db import init_db

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="AI Banking Assistant",
    page_icon="🏦",
    layout="centered"
)

# -----------------------------
# Add project folder to Python path
# -----------------------------
current_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_folder)

# -----------------------------
# Import experiments
# -----------------------------
from experiments.llm_groq import LLMGroq
from experiments.llm_local import LLMLocal

# -----------------------------
# Initialize session state
# -----------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# -----------------------------
# Initialize database
# -----------------------------
init_db()

# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title("AI Banking Assistant")

if not st.session_state.logged_in:
    page = st.sidebar.radio(
        "Go to",
        ["Login", "Create Account"],
        key="auth_menu"
    )
else:
    page = st.sidebar.radio(
        "Go to",
        ["Chatbot", "Admin Analytics", "Logout"],
        key="main_sidebar_menu"
    )

# -----------------------------
# Page logic
# -----------------------------
if page == "Login":
    from pages.Login import show_Login
    show_Login()
elif page == "Create Account":
    from pages.Create_Account import show_Create_Account
    show_Create_Account()
elif page == "Chatbot":
    from pages.Chatbot import show_Chatbot
    show_Chatbot()
elif page == "Admin Analytics":
    from pages.Admin_Analytics import show_admin_analytics
    show_admin_analytics()
elif page == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = None
    st.success("Logged out successfully! Please select a page from the sidebar.")
    st.stop()  # Stop further execution to refresh page

# -----------------------------
# Main page container styling
# -----------------------------
st.markdown("""
<style>
         [data-testid="stSidebarNav"] {
    display: none;
}   
.stApp {
    background: linear-gradient(135deg,#667eea,#764ba2);
    color: white;
}
.card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    color: black;
}
            
div.stButton > button {
    background: linear-gradient(135deg,#ff512f,#dd2476);
    color: white;
    border-radius: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


