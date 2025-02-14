import streamlit as st

def show_current_option():
    """Display the current option header"""
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 🔄 Currently working on Option {st.session_state.current_option}")
    with col2:
        if st.session_state.options_data:
            st.markdown("**Completed options:** " + ", ".join([f"Option {k}" for k in st.session_state.options_data.keys()]))
    st.markdown("---") 