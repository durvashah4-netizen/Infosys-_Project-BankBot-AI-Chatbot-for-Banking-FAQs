import streamlit as st
from database.bank_crud import check_balance, transfer_money, card_details
from core.intent_classifier import detect_intent
from experiments.llm_groq import LLMGroq
from experiments.llm_local import LLMLocal


def show_Chatbot():

    st.set_page_config("BankBot AI", "🤖", layout="centered")

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
        padding: 20px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🤖 AI Banking Assistant")

    # ---------------- SESSION INIT ----------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "step" not in st.session_state:
        st.session_state.step = None
        st.session_state.data = {}

    if "llm_groq" not in st.session_state:
        st.session_state.llm_groq = LLMGroq()

    if "llm_local" not in st.session_state:
        st.session_state.llm_local = LLMLocal()

    llm_groq = st.session_state.llm_groq
    llm_local = st.session_state.llm_local

    # ---------------- CHAT UI ----------------
    user_input = st.text_input("💬 Ask something:", key="chat_input")

    if st.button("Send", key="send_main") and user_input.strip():

        # 🔹 Step-based banking flow
        if st.session_state.step:

            if st.session_state.step == "ask_account":
                acc = user_input
                if st.session_state.intent == "balance":
                    st.session_state.chat_history.append(
                        ("Bot", f"💰 Balance: ₹{check_balance(acc)}")
                    )
                elif st.session_state.intent == "card":
                    cards = card_details(acc)
                    for c in cards:
                        st.session_state.chat_history.append(
                            ("Bot", f"💳 {c[0]} | {c[1]}")
                        )
                st.session_state.step = None

            elif st.session_state.step == "sender":
                st.session_state.data["sender"] = user_input
                st.session_state.step = "receiver"
                st.session_state.chat_history.append(
                    ("Bot", "📥 Enter receiver account number")
                )

            elif st.session_state.step == "receiver":
                st.session_state.data["receiver"] = user_input
                st.session_state.step = "amount"
                st.session_state.chat_history.append(
                    ("Bot", "💸 Enter amount")
                )

            elif st.session_state.step == "amount":
                st.session_state.data["amount"] = float(user_input)
                st.session_state.step = "password"
                st.session_state.chat_history.append(
                    ("Bot", "🔐 Enter password")
                )

            elif st.session_state.step == "password":
                res = transfer_money(
                    st.session_state.data["sender"],
                    st.session_state.data["receiver"],
                    st.session_state.data["amount"],
                    user_input
                )
                st.session_state.chat_history.append(("Bot", res))
                st.session_state.step = None
                st.session_state.data = {}

        # 🔹 New intent detection
        else:
            intent = detect_intent(user_input)
            st.session_state.intent = intent

            if intent in ["balance", "saving", "card"]:
                st.session_state.step = "ask_account"
                st.session_state.chat_history.append(
                    ("Bot", "🔢 Enter account number")
                )

            elif intent == "transfer":
                st.session_state.step = "sender"
                st.session_state.chat_history.append(
                    ("Bot", "📤 Enter sender account number")
                )

            else:
                keywords = ["account", "balance", "bank", "loan"]
                if any(word in user_input.lower() for word in keywords):
                    response = llm_local.ask(user_input)
                else:
                    response = llm_groq.ask(user_input)

                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Bot", response))

    # ---------------- DISPLAY CHAT ----------------
    st.markdown("---")
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**🤖 Bot:** {msg}")
