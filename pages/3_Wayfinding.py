import streamlit as st
import pandas as pd
from utils.session_state import init_session_state

init_session_state()

st.title("Wayfinding Evaluation")

with st.expander("ℹ️ About Wayfinding Features"):
    st.markdown("""
    Wayfinding features are evaluated based on:
    * Signage and visibility
    * Navigation systems
    * Floor markings
    * Information displays
    * Lighting
    * Emergency guidance
    """)

# Basic Wayfinding Features
st.subheader("Basic Wayfinding Features")
col1, col2 = st.columns(2)

with col1:
    signage = st.checkbox("Clear and visible signage")
    floor_marking = st.checkbox("Floor markings and directions")
    level_identification = st.checkbox("Clear level identification")
    exit_markers = st.checkbox("Well-marked exits and entrances")

with col2:
    space_counting = st.checkbox("Space counting system")
    guidance_system = st.checkbox("Electronic guidance system")
    emergency_signs = st.checkbox("Emergency exit signs")
    disabled_parking_signs = st.checkbox("Disabled parking indicators")

# Advanced Features
st.subheader("Advanced Features")
col3, col4 = st.columns(2)

with col3:
    digital_displays = st.selectbox(
        "Digital Information Displays",
        ["None", "Basic", "Advanced", "Smart"]
    )
    
    mobile_app = st.selectbox(
        "Mobile App Integration",
        ["None", "Basic", "Full Integration"]
    )
    
    color_coding = st.checkbox("Color-coded zones/levels")

with col4:
    lighting_quality = st.select_slider(
        "Lighting Quality",
        options=["Poor", "Fair", "Good", "Excellent"]
    )
    
    variable_messaging = st.checkbox("Variable message signs")
    qr_codes = st.checkbox("QR code navigation points")

# Additional Parameters
st.subheader("Supplementary Features")
col5, col6 = st.columns(2)

with col5:
    directory_boards = st.number_input(
        "Number of Directory Boards",
        min_value=0,
        max_value=20,
        value=2
    )
    
    help_points = st.number_input(
        "Number of Help Points",
        min_value=0,
        max_value=20,
        value=2
    )

with col6:
    sign_languages = st.multiselect(
        "Languages on Signs",
        ["English", "Spanish", "Chinese", "Arabic", "Other"]
    )
    
    accessibility_features = st.multiselect(
        "Accessibility Features",
        ["Braille", "Audio Guidance", "Tactile Paths", "Large Print"]
    )

def calculate_wayfinding_los():
    # Count basic features
    basic_features = sum([
        signage, floor_marking, level_identification, 
        exit_markers, space_counting, guidance_system,
        emergency_signs, disabled_parking_signs
    ])
    
    # Advanced features scoring
    advanced_score = 0
    
    # Digital displays
    display_scores = {"None": 0, "Basic": 0.5, "Advanced": 0.75, "Smart": 1}
    advanced_score += display_scores[digital_displays]
    
    # Mobile app
    app_scores = {"None": 0, "Basic": 0.5, "Full Integration": 1}
    advanced_score += app_scores[mobile_app]
    
    # Lighting
    lighting_scores = {"Poor": 0, "Fair": 0.3, "Good": 0.6, "Excellent": 1}
    advanced_score += lighting_scores[lighting_quality]
    
    # Additional features
    advanced_score += 0.2 * (color_coding + variable_messaging + qr_codes)
    
    # Calculate total score
    total_score = basic_features + advanced_score
    
    # Determine LOS
    if total_score >= 10: los = 'A'
    elif total_score >= 8: los = 'B'
    elif total_score >= 6: los = 'C'
    elif total_score >= 4: los = 'D'
    elif total_score >= 2: los = 'E'
    else: los = 'F'
    
    st.session_state['wayfinding_los'] = los
    st.session_state['wayfinding_features'] = total_score
    return los

if st.button("Calculate Wayfinding LOS"):
    los = calculate_wayfinding_los()
    st.metric("Wayfinding LOS", los)
    
    # Display recommendations
    with st.expander("Recommendations"):
        if not signage:
            st.warning("Basic signage is essential - consider adding clear signs")
        if not space_counting:
            st.info("Space counting system could improve efficiency")
        if lighting_quality in ["Poor", "Fair"]:
            st.warning("Consider improving lighting conditions")
        if len(accessibility_features) < 2:
            st.info("Consider adding more accessibility features")

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
        
        # Save all wayfinding parameters
        st.session_state.options_data[st.session_state.current_option].update({
            'signage': signage,
            'floor_marking': floor_marking,
            'level_identification': level_identification,
            'exit_markers': exit_markers,
            'space_counting': space_counting,
            'guidance_system': guidance_system,
            'emergency_signs': emergency_signs,
            'disabled_parking_signs': disabled_parking_signs,
            'digital_displays': digital_displays,
            'mobile_app': mobile_app,
            'color_coding': color_coding,
            'lighting_quality': lighting_quality,
            'variable_messaging': variable_messaging,
            'qr_codes': qr_codes,
            'directory_boards': directory_boards,
            'help_points': help_points,
            'sign_languages': sign_languages,
            'accessibility_features': accessibility_features,
            'wayfinding_los': st.session_state.get('wayfinding_los', 'N/A'),
            'wayfinding_features': st.session_state.get('wayfinding_features', 0)
        })
        
        st.success(f"Option {st.session_state.current_option} wayfinding data saved successfully!") 