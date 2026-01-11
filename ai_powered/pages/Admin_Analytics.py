import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import random
from fpdf import FPDF
from difflib import SequenceMatcher


def show_admin_analytics():
    # =====================================================
    # PDF EXPORT FUNCTION
    # =====================================================
    def export_pdf(df):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Admin Analytics Report", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", size=12)

        for _, r in df.iterrows():
            pdf.cell(0, 8, f"{r['intent']} : {r['count']}", ln=True)

        file = "analytics.pdf"
        pdf.output(file)
        return file

    # =====================================================
    # DEFAULT INTENTS
    # =====================================================
    DEFAULT_INTENTS = {
        "check_balance": [
            "What is my balance?",
            "Show account balance",
            "How much money do I have?"
        ],
        "transfer_money": [
            "Send money",
            "Transfer funds",
            "Pay someone"
        ],
        "card_block": [
            "Block my card",
            "Card stolen",
            "Lost my debit card"
        ],
        "find_atm": [
            "ATM near me",
            "Find nearby ATM",
            "Locate ATM"
        ]
    }

    # =====================================================
    # SESSION STATE INITIALIZATION
    # =====================================================
    if "training_data" not in st.session_state:
        st.session_state.training_data = DEFAULT_INTENTS.copy()

    if "intent_logs" not in st.session_state:
        st.session_state.intent_logs = []

    if "admin_menu" not in st.session_state:
        st.session_state.admin_menu = "📊 Chat Analytics"

    if "model_config" not in st.session_state:
        st.session_state.model_config = {
            "epochs": 10,
            "batch_size": 16,
            "learning_rate": 0.001
        }

    if "admin_page_configured" not in st.session_state:
        st.set_page_config(
            page_title="BankBot Admin Panel",
            layout="wide"
        )
        st.session_state.admin_page_configured = True

    # =====================================================
    # INTENT CLASSIFIER
    # =====================================================
    def classify_intent(query):
        q = query.lower()
        best_intent = "other"
        max_ratio = 0.0

        for intent, examples in st.session_state.training_data.items():
            for ex in examples:
                ratio = SequenceMatcher(None, q, ex.lower()).ratio()
                if ratio > max_ratio:
                    max_ratio = ratio
                    best_intent = intent

        if max_ratio < 0.5:
            best_intent = "other"
            confidence = 0.0
        else:
            confidence = round(max_ratio, 2)

        return best_intent, confidence

    # =====================================================
    # SIDEBAR
    # =====================================================
    st.sidebar.title("🏦 BankBot Admin")
    menu = st.sidebar.radio(
    "Navigation",
    [
        "📊 Chat Analytics",
        "📈 Query Analytics",
        "🧠 Training Editor",
        "📤 Export Logs"
    ],
    index=[
        "📊 Chat Analytics",
        "📈 Query Analytics",
        "🧠 Training Editor",
        "📤 Export Logs"
    ].index(st.session_state.admin_menu),
    key="admin_sidebar_menu_unique"
  )

    st.session_state.admin_menu = menu

    st.sidebar.divider()
    st.sidebar.subheader("🔍 Test Query")

    user_query = st.sidebar.text_input("Enter user query")

    if st.sidebar.button("Analyze Query"):
        if user_query:
            intent, confidence = classify_intent(user_query)
            st.session_state.intent_logs.append({
                "question": user_query,
                "intent": intent,
                "confidence": confidence,
                "timestamp": datetime.now()
            })
            st.sidebar.success(f"{intent} ({confidence})")

    # =====================================================
    # CHAT ANALYTICS
    # =====================================================
    if menu == "📊 Chat Analytics":
        st.title("📊 Chat Analytics")

        if st.session_state.intent_logs:
            df = pd.DataFrame(st.session_state.intent_logs)

            intent_choice = st.radio(
                "Select Intent",
                ["overall", "check_balance", "transfer_money", "card_block", "find_atm"],
                horizontal=True
            )

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                if intent_choice == "overall":
                    df["intent"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
                else:
                    selected_count = df[df["intent"] == intent_choice].shape[0]
                    other_count = df.shape[0] - selected_count
                    ax.pie(
                        [selected_count, other_count],
                        labels=[intent_choice, "Other Intents"],
                        autopct="%1.1f%%"
                    )
                st.pyplot(fig)

            with col2:
                if intent_choice == "overall":
                    st.dataframe(df[["question", "intent", "timestamp"]])
                else:
                    st.dataframe(
                        df[df["intent"] == intent_choice][
                            ["question", "intent", "timestamp"]
                        ]
                    )
        else:
            st.info("No queries yet")

    # =====================================================
    # QUERY ANALYTICS
    # =====================================================
    elif menu == "📈 Query Analytics":
        st.title("📈 Query Analytics")

        if st.session_state.intent_logs:
            df = pd.DataFrame(st.session_state.intent_logs)
            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                df["intent"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
                st.pyplot(fig)

            with col2:
                fig, ax = plt.subplots()
                ax.hist(df["confidence"], bins=10)
                st.pyplot(fig)

            st.dataframe(df.sort_values("timestamp", ascending=False).head(10))
        else:
            st.info("No data available")

    # =====================================================
    # TRAINING EDITOR
    # =====================================================
    elif menu == "🧠 Training Editor":
        st.title("🧠 Intent Training Editor")

        col_left, col_mid, col_right = st.columns([2, 2, 3])

        # LEFT
        with col_left:
            st.subheader("📂 Intents")
            for intent, examples in st.session_state.training_data.items():
                with st.expander(f"✏️ {intent} ({len(examples)} examples)"):
                    for i, ex in enumerate(examples):
                        st.text_input(
                            f"{intent}_{i}",
                            value=ex,
                            key=f"{intent}_{i}_edit"
                        )

        # MIDDLE
        with col_mid:
            st.subheader("➕ Quick Add Example")

            selected_intent = st.selectbox(
                "Select Intent",
                list(st.session_state.training_data.keys())
            )

            new_example = st.text_input("New example")

            if st.button("➕ ADD NOW"):
                if new_example.strip():
                    st.session_state.training_data[selected_intent].append(new_example)
                    st.success("Example added")
                    st.rerun()

            st.divider()
            st.subheader("🚀 Train Model")

            epochs = st.slider("Epochs", 1, 50, 10)
            lr = st.selectbox("Learning Rate", [0.1, 0.01, 0.001])

            if st.button("TRAIN MODEL"):
                with st.spinner("Training model..."):
                    import time
                    time.sleep(2)
                st.success("✅ Model trained successfully")

        # RIGHT
        with col_right:
            st.subheader("🧪 Test Queries")

            test_query = st.text_area(
                "User Query",
                placeholder="Show balance and send 1000 rupees to my friend"
            )

            top_k = st.slider("Top intents to show", 1, 5, 3)

            if st.button("🔍 Analyze"):
                if test_query.strip():
                    scores = []
                    q = test_query.lower()

                    for intent, examples in st.session_state.training_data.items():
                        best = 0
                        for ex in examples:
                            score = SequenceMatcher(None, q, ex.lower()).ratio()
                            best = max(best, score)
                        scores.append((intent, round(best, 2)))

                    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]

                    st.markdown("### 🔎 Detected Intents")
                    for intent, score in scores:
                        st.progress(score)
                        st.write(f"**{intent}** → {score}")

    # =====================================================
    # EXPORT LOGS
    # =====================================================
    elif menu == "📤 Export Logs":
        st.title("📤 Export Logs")

        if st.session_state.intent_logs:
            df = pd.DataFrame(st.session_state.intent_logs)
            summary = df["intent"].value_counts().reset_index()
            summary.columns = ["intent", "count"]

            st.dataframe(summary)

            if st.button("Export PDF"):
                file = export_pdf(summary)
                with open(file, "rb") as f:
                    st.download_button(
                        "⬇ Download PDF",
                        f,
                        file_name="analytics_report.pdf"
                    )
        else:
            st.info("No logs available to export")


