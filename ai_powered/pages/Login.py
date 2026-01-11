import streamlit as st
from database.bank_crud import get_user
from database.security import verify_password
import sys
import os

# Ensure ai_powered folder is in path
current_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_folder)


def show_Login():

    # ---------------- PAGE CONFIG ----------------
    st.set_page_config(
        page_title="Login",
        page_icon="🏦",
        layout="centered"
    )

    # ---------------- SESSION STATE INIT ----------------
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    # ---------------- CSS ----------------
    st.markdown("""
    <style>
                [data-testid="stSidebarNav"] {
    visibility: hidden;
}
    .stApp {
        background: linear-gradient(135deg,#667eea,#764ba2);
    }

    .card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }

    div.stButton > button {
        background: linear-gradient(135deg,#ff512f,#dd2476);
        color: white;
        border-radius: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- UI ----------------
    st.title("🏦 BankBot Login")

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        username = st.text_input("👤 Username")
        password = st.text_input("🔐 Password", type="password")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- LOGIN LOGIC ----------------
    if st.button("Login"):
        user = get_user(username)

        if user and verify_password(password, user[1]):
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.rerun()
        