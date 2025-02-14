import streamlit as st
import pandas as pd

st.title("Geometry Configuration Evaluation")

with st.expander("ℹ️ About Geometry Configurations"):
    st.markdown("""
    Geometry configurations are evaluated based on:
    * Parking space dimensions
    * Aisle width
    * Column spacing
    * Clearance height
    * Parking angle
    * Turn radius
    """)

# Basic Dimensions
st.subheader("Basic Dimensions")
col1, col2 = st.columns(2)

with col1:
    space_width = st.number_input(
        "Parking Space Width (ft)",
        min_value=7.0,
        max_value=10.0,
        value=8.5,
        step=0.1
    )
    
    space_length = st.number_input(
        "Parking Space Length (ft)",
        min_value=15.0,
        max_value=20.0,
        value=18.0,
        step=0.1
    )

with col2:
    aisle_width = st.number_input(
        "Aisle Width (ft)",
        min_value=16.0,
        max_value=25.0,
        value=20.0,
        step=0.1
    )
    
    clearance = st.number_input(
        "Clearance Height (ft)",
        min_value=6.0,
        max_value=10.0,
        value=7.0,
        step=0.1
    )

# Additional Parameters
st.subheader("Additional Parameters")
col3, col4 = st.columns(2)

with col3:
    parking_angle = st.selectbox(
        "Parking Angle",
        ["90°", "60°", "45°", "30°"]
    )
    
    column_spacing = st.number_input(
        "Column Spacing (ft)",
        min_value=15.0,
        max_value=30.0,
        value=20.0
    )
    
    turn_radius = st.number_input(
        "Turn Radius (ft)",
        min_value=10.0,
        max_value=25.0,
        value=15.0
    )

with col4:
    buffer_zone = st.number_input(
        "Buffer Zone Width (ft)",
        min_value=0.0,
        max_value=5.0,
        value=1.0
    )
    
    end_island_width = st.number_input(
        "End Island Width (ft)",
        min_value=0.0,
        max_value=10.0,
        value=4.0
    )
    
    wheel_stops = st.checkbox("Wheel Stops Present")

def calculate_geometry_los():
    # Store parameters in session state
    st.session_state['space_width'] = space_width
    st.session_state['aisle_width'] = aisle_width
    
    # Enhanced LOS calculation logic
    base_score = 0
    
    # Space width evaluation
    if space_width >= 9.0: base_score += 2
    elif space_width >= 8.5: base_score += 1.5
    elif space_width >= 8.0: base_score += 1
    
    # Aisle width evaluation
    if aisle_width >= 24.0: base_score += 2
    elif aisle_width >= 22.0: base_score += 1.5
    elif aisle_width >= 20.0: base_score += 1
    
    # Parking angle consideration
    angle_scores = {"90°": 1, "60°": 0.8, "45°": 0.6, "30°": 0.4}
    base_score += angle_scores[parking_angle]
    
    # Determine LOS
    if base_score >= 4.5: los = 'A'
    elif base_score >= 3.5: los = 'B'
    elif base_score >= 2.5: los = 'C'
    elif base_score >= 1.5: los = 'D'
    elif base_score >= 0.5: los = 'E'
    else: los = 'F'
    
    st.session_state['geometry_los'] = los
    return los

if st.button("Calculate Geometry LOS"):
    los = calculate_geometry_los()
    st.metric("Geometry Configuration LOS", los)
    
    # Display recommendations
    with st.expander("Recommendations"):
        if space_width < 8.5:
            st.warning("Consider wider parking spaces for better maneuverability")
        if aisle_width < 22.0:
            st.warning("Wider aisles recommended for easier navigation")
        if not wheel_stops and parking_angle == "90°":
            st.info("Consider adding wheel stops for 90° parking")

# Add at the bottom of the file, after the LOS calculation
st.divider()
col1, col2 = st.columns([3, 1])
with col1:
    st.write(f"Currently working on Option {st.session_state.current_option}")
with col2:
    if st.button("Save Option Results"):
        # Save current option data
        if st.session_state.current_option not in st.session_state.options_data:
            st.session_state.options_data[st.session_state.current_option] = {}
        
        # Save all geometry parameters
        st.session_state.options_data[st.session_state.current_option].update({
            'space_width': space_width,
            'space_length': space_length,
            'aisle_width': aisle_width,
            'clearance': clearance,
            'parking_angle': parking_angle,
            'column_spacing': column_spacing,
            'turn_radius': turn_radius,
            'buffer_zone': buffer_zone,
            'end_island_width': end_island_width,
            'wheel_stops': wheel_stops,
            'geometry_los': st.session_state.get('geometry_los', 'N/A')
        })
        
        st.success(f"Option {st.session_state.current_option} geometry data saved successfully!") 