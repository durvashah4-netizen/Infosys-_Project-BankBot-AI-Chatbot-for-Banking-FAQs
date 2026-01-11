import streamlit as st
from database.bank_crud import create_user, create_account
import sys
import os

# Ensure ai_powered folder is in path
current_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_folder)


def show_Create_Account():

    st.set_page_config(
        page_title="Create Account",
        page_icon="🏦",
        layout="centered"
    )

    # ---------------- UI STYLE ----------------
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

    st.markdown("## 🏦 Create New Bank Account")

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        username = st.text_input("👤 Username")
        login_pwd = st.text_input("🔐 Login Password", type="password")
        acc_no = st.text_input("🏦 Account Number")

        acc_type = st.selectbox(
            "📂 Account Type",
            ["Savings", "Current"]
        )

        balance = st.number_input(
            "💰 Initial Balance",
            min_value=0.0,
            value=50000.0,
            step=1000.0
        )

        acc_pwd = st.text_input(
            "🔑 Account Password",
            type="password"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- CREATE BUTTON ----------------
    if st.button("✅ Create Account"):
        if not all([username, login_pwd, acc_no, acc_pwd]):
            st.warning("⚠ Please fill all required fields")
        else:
            try:
                uid = create_user(username, login_pwd)
                create_account(uid, acc_no, acc_type, balance, acc_pwd)
                st.success("🎉 Account created successfully!")
                st.info("➡ Now go to Login page")
            except Exception:
                st.error("❌ Username or account number already exists")
