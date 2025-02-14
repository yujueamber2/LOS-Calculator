import streamlit as st
import pandas as pd
from utils.session_state import init_session_state

init_session_state()

st.title("Evaluation Rules and Reference Data")

# LOS Criteria Tables
st.header("LOS Criteria")

with st.expander("Ramping System LOS Criteria"):
    ramping_criteria = pd.DataFrame({
        'LOS': ['A', 'B', 'C', 'D', 'E', 'F'],
        'Slope (%)': ['≤6.0', '≤8.0', '≤10.0', '≤12.0', '≤15.0', '>15.0'],
        'Max Turns': ['2', '3', '4', '5', '6', '>6'],
        'Description': [
            'Excellent ramping conditions',
            'Good ramping conditions',
            'Fair ramping conditions',
            'Poor ramping conditions',
            'Very poor ramping conditions',
            'Unacceptable conditions'
        ]
    })
    st.table(ramping_criteria)

with st.expander("Geometry Configuration LOS Criteria"):
    geometry_criteria = pd.DataFrame({
        'LOS': ['A', 'B', 'C', 'D', 'E', 'F'],
        'Space Width (ft)': ['≥9.0', '≥8.5', '≥8.0', '≥7.5', '≥7.0', '<7.0'],
        'Aisle Width (ft)': ['≥24.0', '≥22.0', '≥20.0', '≥18.0', '≥16.0', '<16.0'],
        'Description': [
            'Excellent maneuvering space',
            'Good maneuvering space',
            'Fair maneuvering space',
            'Poor maneuvering space',
            'Very poor maneuvering space',
            'Unacceptable conditions'
        ]
    })
    st.table(geometry_criteria)

with st.expander("Wayfinding LOS Criteria"):
    wayfinding_criteria = pd.DataFrame({
        'LOS': ['A', 'B', 'C', 'D', 'E', 'F'],
        'Features Required': ['6', '5', '4', '3', '2', '≤1'],
        'Description': [
            'Comprehensive wayfinding system',
            'Very good wayfinding system',
            'Good wayfinding system',
            'Basic wayfinding system',
            'Minimal wayfinding system',
            'Inadequate wayfinding'
        ]
    })
    st.table(wayfinding_criteria)

# References and Notes
with st.expander("📚 References and Notes"):
    st.markdown("""
    * All criteria are based on industry standards and best practices
    * LOS calculations consider weighted averages of different components
    * Regular evaluation and updates are recommended
    * Local regulations may require specific adjustments
    """) 