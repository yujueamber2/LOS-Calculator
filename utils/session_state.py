import streamlit as st

def init_session_state():
    """Initialize session state variables"""
    if 'current_option' not in st.session_state:
        st.session_state.current_option = 1
    if 'options_data' not in st.session_state:
        st.session_state.options_data = {}
    if 'max_options' not in st.session_state:
        st.session_state.max_options = 3 