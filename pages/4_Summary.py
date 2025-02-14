import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.session_state import init_session_state
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

def calculate_overall_los(ramping_los, geometry_los, wayfinding_los):
    weights = {'Ramping': 0.4, 'Geometry': 0.3, 'Wayfinding': 0.3}
    scores = {
        'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0
    }
    
    total_score = (
        weights['Ramping'] * scores[ramping_los] +
        weights['Geometry'] * scores[geometry_los] +
        weights['Wayfinding'] * scores[wayfinding_los]
    )
    
    if total_score >= 4.5: return 'A'
    elif total_score >= 3.5: return 'B'
    elif total_score >= 2.5: return 'C'
    elif total_score >= 1.5: return 'D'
    elif total_score >= 0.5: return 'E'
    else: return 'F'

st.title("Summary of Parking LOS")

# Project Information
with st.expander("Project Details"):
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name")
        location = st.text_input("Location")
        date = st.date_input("Date")
    with col2:
        analyst = st.text_input("Analyst")
        reviewer = st.text_input("Reviewer")
        notes = st.text_area("Notes")

# Compare all options
if st.session_state.options_data:
    st.header("Options Comparison")
    
    # Create comparison dataframe
    comparison_data = []
    for option_num, option_data in st.session_state.options_data.items():
        option_results = {
            'Option': f"Option {option_num}",
            'Ramping LOS': option_data.get('ramping_los', 'N/A'),
            'Geometry LOS': option_data.get('geometry_los', 'N/A'),
            'Wayfinding LOS': option_data.get('wayfinding_los', 'N/A')
        }
        
        # Calculate overall LOS if all components are available
        if all(option_data.get(f'{component}_los', 'N/A') != 'N/A' 
               for component in ['ramping', 'geometry', 'wayfinding']):
            option_results['Overall LOS'] = calculate_overall_los(
                option_data['ramping_los'],
                option_data['geometry_los'],
                option_data['wayfinding_los']
            )
        else:
            option_results['Overall LOS'] = 'N/A'
            
        comparison_data.append(option_results)
    
    # Display comparison table
    comparison_df = pd.DataFrame(comparison_data)
    st.table(comparison_df)
    
    # Detailed comparison for each option
    st.header("Detailed Option Analysis")
    for option_num, option_data in st.session_state.options_data.items():
        with st.expander(f"Option {option_num} Details"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("Ramping System")
                st.metric("LOS", option_data.get('ramping_los', 'N/A'))
                st.write("Key Factors:")
                st.write("- Ramp Type:", option_data.get('ramp_type', 'N/A'))
                st.write("- Slope:", option_data.get('slope', 'N/A'), "%")
            
            with col2:
                st.subheader("Geometry")
                st.metric("LOS", option_data.get('geometry_los', 'N/A'))
                st.write("Key Dimensions:")
                st.write("- Space Width:", option_data.get('space_width', 'N/A'), "ft")
                st.write("- Aisle Width:", option_data.get('aisle_width', 'N/A'), "ft")
            
            with col3:
                st.subheader("Wayfinding")
                st.metric("LOS", option_data.get('wayfinding_los', 'N/A'))
                st.write("Features Present:", option_data.get('wayfinding_features', 'N/A'))
            
            # Recommendations
            st.subheader("Recommendations")
            ramping_los = option_data.get('ramping_los', 'N/A')
            geometry_los = option_data.get('geometry_los', 'N/A')
            wayfinding_los = option_data.get('wayfinding_los', 'N/A')
            
            if ramping_los < 'B':
                st.warning("Consider improving ramp system design")
            if geometry_los < 'B':
                st.warning("Review parking space and aisle dimensions")
            if wayfinding_los < 'B':
                st.warning("Enhance wayfinding features")
    else:
        st.info("No options have been evaluated yet. Please complete at least one evaluation.")

    # Detailed Parameters Comparison
    st.subheader("Detailed Parameters Comparison")
    
    # Organize parameters by category
    ramping_params = {
        "Ramping System Parameters": [
            'Ramp Type', 'Slope (%)', 'Turns', 'Flow',
            'Vertical Clearance (ft)', 'Surface Condition'
        ]
    }
    
    geometry_params = {
        "Geometry Parameters": [
            'Space Width (ft)', 'Space Length (ft)', 'Aisle Width (ft)',
            'Parking Angle', 'Column Spacing (ft)'
        ]
    }
    
    wayfinding_params = {
        "Wayfinding Parameters": [
            'Digital Displays', 'Lighting Quality',
            'Space Counting', 'Guidance System'
        ]
    }

    # Create three columns for side-by-side comparison
    cols = st.columns(len(st.session_state.options_data))
    
    # Display parameters by category for each option
    for idx, (option_num, option_data) in enumerate(st.session_state.options_data.items()):
        with cols[idx]:
            st.markdown(f"### Option {option_num}")
            
            # Display Ramping parameters
            st.markdown("#### 🚗 Ramping System")
            for param in ramping_params["Ramping System Parameters"]:
                value = option_data.get(param.lower().replace(' ', '_').replace('(%)', ''), 'N/A')
                st.markdown(f"**{param}:** {value}")
            
            # Display Geometry parameters
            st.markdown("#### 📐 Geometry")
            for param in geometry_params["Geometry Parameters"]:
                value = option_data.get(param.lower().replace(' ', '_').replace('(%)', ''), 'N/A')
                st.markdown(f"**{param}:** {value}")
            
            # Display Wayfinding parameters
            st.markdown("#### 🔍 Wayfinding")
            for param in wayfinding_params["Wayfinding Parameters"]:
                value = option_data.get(param.lower().replace(' ', '_'), 'N/A')
                st.markdown(f"**{param}:** {value}")

def generate_pdf_report():
    """Generate a professionally formatted PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    elements = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12
    )
    
    # Title
    elements.append(Paragraph("Parking Facility LOS Analysis Report", title_style))
    elements.append(Spacer(1, 12))
    
    # Project Information
    elements.append(Paragraph("Project Information", heading_style))
    project_info = [
        ["Project Name:", st.session_state.get('project_name', 'N/A')],
        ["Location:", st.session_state.get('location', 'N/A')],
        ["Date:", str(st.session_state.get('date', 'N/A'))],
        ["Analyst:", st.session_state.get('analyst', 'N/A')],
        ["Reviewer:", st.session_state.get('reviewer', 'N/A')]
    ]
    
    t = Table(project_info, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))
    
    # LOS Summary
    elements.append(Paragraph("LOS Summary", heading_style))
    los_data = [["Option", "Ramping LOS", "Geometry LOS", "Wayfinding LOS", "Overall LOS"]]
    
    for option_num, option_data in st.session_state.options_data.items():
        los_row = [
            f"Option {option_num}",
            option_data.get('ramping_los', 'N/A'),
            option_data.get('geometry_los', 'N/A'),
            option_data.get('wayfinding_los', 'N/A'),
            calculate_overall_los(
                option_data.get('ramping_los', 'N/A'),
                option_data.get('geometry_los', 'N/A'),
                option_data.get('wayfinding_los', 'N/A')
            ) if all(option_data.get(f'{c}_los', 'N/A') != 'N/A' for c in ['ramping', 'geometry', 'wayfinding']) else 'N/A'
        ]
        los_data.append(los_row)
    
    t = Table(los_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)
    
    # Add detailed parameters for each option
    for option_num, option_data in st.session_state.options_data.items():
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"Option {option_num} Details", heading_style))
        
        # Create tables for each category
        for category, params in [
            ("Ramping System Parameters", ramping_params["Ramping System Parameters"]),
            ("Geometry Parameters", geometry_params["Geometry Parameters"]),
            ("Wayfinding Parameters", wayfinding_params["Wayfinding Parameters"])
        ]:
            elements.append(Paragraph(category, styles['Heading3']))
            param_data = [[param, option_data.get(param.lower().replace(' ', '_').replace('(%)', ''), 'N/A')] 
                         for param in params]
            
            t = Table(param_data, colWidths=[3*inch, 3*inch])
            t.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(t)
            elements.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Update the download button section
st.header("Download Report")
pdf_buffer = generate_pdf_report()
st.download_button(
    label="Download Detailed Report (PDF)",
    data=pdf_buffer,
    file_name="parking_los_report.pdf",
    mime="application/pdf"
)