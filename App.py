import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Academic Tracker",
    page_icon="📚",
    layout="centered"
)

# Minimal Aesthetic Styling
st.markdown("""
    <style>
    .main {
        background-color: #fafafa;
    }
    h1 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 500;
        color: #111111;
        letter-spacing: -0.5px;
    }
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# App Content
st.title("Academic Tracker")
st.write("A clean and minimal space to manage your coursework and daily progress.")

# Simple input section
task_name = st.text_input("Add a new task")
if st.button("Save Task"):
    if task_name:
        st.success(f"Task added: {task_name}")
    else:
        st.warning("Please enter a task name.")
