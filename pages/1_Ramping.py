import streamlit as st
import pandas as pd
from utils.session_state import init_session_state
from utils.common import show_current_option

init_session_state()

# Show current option at the top
show_current_option()

st.title("Ramping System Evaluation")

with st.expander("ℹ️ About Ramping Systems"):
    st.markdown("""
    Ramping systems are evaluated based on:
    * Type of ramp (straight, curved, helix)
    * Slope percentage
    * Number of turns
    * Traffic flow direction
    * Vertical clearance
    * Surface conditions
    """)

# Input sections
col1, col2 = st.columns(2)

with col1:
    ramp_type = st.selectbox(
        "Select Ramp Type",
        ["Straight", "Curved", "Helix"]
    )
    
    slope = st.slider(
        "Ramp Slope (%)",
        min_value=0.0,
        max_value=20.0,
        value=6.0,
        step=0.1
    )
    
    turns = st.number_input(
        "Number of Turns",
        min_value=0,
        max_value=10,
        value=0
    )

with col2:
    flow = st.radio(
        "Traffic Flow",
        ["One-way", "Two-way"]
    )
    
    vertical_clearance = st.number_input(
        "Vertical Clearance (ft)",
        min_value=6.0,
        max_value=12.0,
        value=7.0,
        step=0.1
    )
    
    surface_condition = st.selectbox(
        "Surface Condition",
        ["Excellent", "Good", "Fair", "Poor"]
    )

# Additional Parameters
st.subheader("Additional Parameters")
col3, col4 = st.columns(2)

with col3:
    transition_length = st.number_input(
        "Transition Length (ft)",
        min_value=0.0,
        max_value=50.0,
        value=10.0
    )
    
    ramp_width = st.number_input(
        "Ramp Width (ft)",
        min_value=8.0,
        max_value=24.0,
        value=12.0
    )

with col4:
    lighting_level = st.selectbox(
        "Lighting Level",
        ["High", "Medium", "Low"]
    )
    
    drainage_system = st.selectbox(
        "Drainage System",
        ["Excellent", "Adequate", "Poor"]
    )

def calculate_ramping_los():
    # Store parameters in session state
    st.session_state['ramp_type'] = ramp_type
    st.session_state['slope'] = slope
    
    # Enhanced LOS calculation logic
    base_score = 0
    
    # Slope evaluation
    if slope <= 6.0: base_score += 2
    elif slope <= 8.0: base_score += 1.5
    elif slope <= 10.0: base_score += 1
    
    # Turns impact
    if turns <= 2: base_score += 1
    elif turns <= 4: base_score += 0.5
    
    # Flow consideration
    if flow == "One-way": base_score += 1
    
    # Surface condition
    condition_scores = {"Excellent": 1, "Good": 0.75, "Fair": 0.5, "Poor": 0}
    base_score += condition_scores[surface_condition]
    
    # Determine LOS
    if base_score >= 4.5: los = 'A'
    elif base_score >= 3.5: los = 'B'
    elif base_score >= 2.5: los = 'C'
    elif base_score >= 1.5: los = 'D'
    elif base_score >= 0.5: los = 'E'
    else: los = 'F'
    
    st.session_state['ramping_los'] = los
    return los

if st.button("Calculate Ramping LOS"):
    los = calculate_ramping_los()
    st.metric("Ramping System LOS", los)
    
    # Display recommendations based on inputs
    with st.expander("Recommendations"):
        if slope > 8.0:
            st.warning("Consider reducing ramp slope for better accessibility")
        if turns > 4:
            st.warning("High number of turns may impact user experience")
        if surface_condition in ["Fair", "Poor"]:
            st.warning("Surface condition improvements recommended")

# At the bottom, remove the current option display and keep only the save button
st.divider()
if st.button("Save Option Results"):
    # Save current option data
    if st.session_state.current_option not in st.session_state.options_data:
        st.session_state.options_data[st.session_state.current_option] = {}
    
    # Save all ramping parameters
    st.session_state.options_data[st.session_state.current_option].update({
        'ramp_type': ramp_type,
        'slope': slope,
        'turns': turns,
        'flow': flow,
        'vertical_clearance': vertical_clearance,
        'surface_condition': surface_condition,
        'transition_length': transition_length,
        'ramp_width': ramp_width,
        'lighting_level': lighting_level,
        'drainage_system': drainage_system,
        'ramping_los': st.session_state.get('ramping_los', 'N/A')
    })
    
    st.success(f"Option {st.session_state.current_option} ramping data saved successfully!") 