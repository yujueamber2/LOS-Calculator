import streamlit as st
from utils.session_state import init_session_state

st.set_page_config(
    page_title="Parking LOS Calculator",
    page_icon="🅿️",
    layout="wide"
)

init_session_state()

def main():
    st.title("Parking LOS Calculator")
    
    # Option management section
    st.subheader("Design Options Management")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display current options status
        st.write(f"Currently working on Option {st.session_state.current_option}")
        if st.session_state.options_data:
            st.write("Completed options:", ", ".join([f"Option {k}" for k in st.session_state.options_data.keys()]))
    
    with col2:
        # Option management buttons
        if len(st.session_state.options_data) < st.session_state.max_options:
            if st.button("Create New Option"):
                st.session_state.current_option = len(st.session_state.options_data) + 1
                st.rerun()
        
        if st.session_state.options_data:
            option_to_modify = st.selectbox(
                "Modify existing option",
                options=list(st.session_state.options_data.keys())
            )
            if st.button("Load Selected Option"):
                st.session_state.current_option = option_to_modify
                # Load the option data into session state
                for key, value in st.session_state.options_data[option_to_modify].items():
                    st.session_state[key] = value
                st.rerun()

    st.markdown("""
    Welcome to the Parking Level of Service (LOS) Calculator. This tool helps you evaluate parking facilities 
    based on multiple criteria including:
    * Ramping Systems
    * Geometry Configurations
    * Wayfinding Features
    
    You can create up to 3 different design options and compare them.
    """)
    
    with st.expander("ℹ️ How to use this calculator"):
        st.markdown("""
        1. Create a new design option or modify existing ones
        2. Navigate through different evaluation pages using the sidebar
        3. Input the required parameters in each section
        4. Save your evaluation results for each option
        5. Compare different options in the Summary page
        """)

if __name__ == "__main__":
    main() 