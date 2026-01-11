import streamlit as st
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate

# ---------------- Configuration ----------------
MODEL_PATH = r"C:\Users\Durva shah\Downloads\Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"

st.set_page_config(page_title="Local Llama Chatbot")
st.title("🦙 Local Llama 3.1 (8B) Chatbot")
class LLMLocal:
    def __init__(self):
        self.model = None
        self.prompt_template = "You are a helpful AI.\nQuestion: {question}\nAnswer step by step:"

    def load_model(self, model):
        """Assign the already loaded LlamaCpp model from session state."""
        self.model = model

    def ask(self, question):
        if self.model is None:
            return "❌ Model not loaded yet."
        prompt = self.prompt_template.format(question=question)
        # LlamaCpp call
        return self.model(prompt)



# ---------------- Cached model loader ----------------
@st.cache_resource
def load_model():
    """
    Load the LlamaCpp model once and reuse across sessions.
    """
    return LlamaCpp(
        model_path=MODEL_PATH,
        n_ctx=8192,
        n_threads=8,
        n_gpu_layers=0,
        temperature=0.3,
    )


# ---------------- Session state initialization ----------------
if "llm" not in st.session_state:
    st.session_state.llm = None
    st.session_state.model_loaded = False


# ---------------- UI: Load model button ----------------
if not st.session_state.model_loaded:
    st.info("Click the button to load the model (first time only).")

    if st.button("Load model"):
        with st.spinner("Loading model... this may take a few minutes"):
            st.session_state.llm = load_model()
            st.session_state.model_loaded = True
        st.success("✅ Model loaded!")
        st.stop()   # refresh the app after loading

# ---------------- Once model is loaded ----------------
else:
    llm = st.session_state.llm

    # Prompt template
    prompt = PromptTemplate.from_template(
        "You are a helpful AI.\nQuestion: {question}\nAnswer step by step:"
    )
    chain = prompt | llm

    # User input
    user_input = st.text_input("Enter your question:")

    if st.button("Send"):
        if not user_input.strip():
            st.warning("Please enter a question!")
        else:
            with st.spinner("Thinking..."):
                result = chain.invoke({"question": user_input})
            st.subheader("Response:")
            st.write(result)
