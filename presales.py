import streamlit as st
from enum import Enum

# Enum for each step in the wizard
class Step(Enum):
    OPPORTUNITY_ASSESSMENT = 1
    V3_QUALIFICATION = 2
    SMART_BUILDINGS = 3
    ASSET_MANAGEMENT = 4
    COLD_CHAIN = 5
    WASTE_MANAGEMENT = 6
    V5_QUALIFICATION = 7
    BESPOKE_QUALIFICATION = 8
    FINANCIAL_FEASIBILITY = 9
    RESULT = 10

# Initialize session state for navigation and responses
if 'current_step' not in st.session_state:
    st.session_state.current_step = Step.OPPORTUNITY_ASSESSMENT
if 'responses' not in st.session_state:
    st.session_state.responses = {}

# Function to move to the next step
def next_step():
    # Ensure the decision-making process works as expected based on input
    if st.session_state.current_step == Step.OPPORTUNITY_ASSESSMENT:
        if st.session_state.responses.get('v3_vertical') == 'Yes':
            st.session_state.current_step = Step.V3_QUALIFICATION
        else:
            st.session_state.current_step = Step.V5_QUALIFICATION
    elif st.session_state.current_step == Step.V3_QUALIFICATION:
        v3_vertical_type = st.session_state.responses.get('v3_vertical_type')
        if v3_vertical_type == "Smart Buildings":
            st.session_state.current_step = Step.SMART_BUILDINGS
        elif v3_vertical_type == "Asset Management":
            st.session_state.current_step = Step.ASSET_MANAGEMENT
        elif v3_vertical_type == "Cold Chain Monitoring":
            st.session_state.current_step = Step.COLD_CHAIN
        elif v3_vertical_type == "Waste Management":
            st.session_state.current_step = Step.WASTE_MANAGEMENT
        else:
            st.write("Please select a vertical.")
    elif st.session_state.current_step == Step.SMART_BUILDINGS:
        st.session_state.current_step = Step.RESULT
    elif st.session_state.current_step == Step.ASSET_MANAGEMENT:
        st.session_state.current_step = Step.RESULT
    elif st.session_state.current_step == Step.COLD_CHAIN:
        st.session_state.current_step = Step.RESULT
    elif st.session_state.current_step == Step.WASTE_MANAGEMENT:
        st.session_state.current_step = Step.RESULT
    elif st.session_state.current_step == Step.V5_QUALIFICATION:
        st.session_state.current_step = Step.BESPOKE_QUALIFICATION
    elif st.session_state.current_step == Step.BESPOKE_QUALIFICATION:
        st.session_state.current_step = Step.FINANCIAL_FEASIBILITY
    elif st.session_state.current_step == Step.FINANCIAL_FEASIBILITY:
        st.session_state.current_step = Step.RESULT

# Function to move to the previous step
def previous_step():
    if st.session_state.current_step != Step.OPPORTUNITY_ASSESSMENT:
        st.session_state.current_step = Step(int(st.session_state.current_step.value) - 1)

# UI for progress bar and navigation buttons
def render_navigation():
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.session_state.current_step != Step.OPPORTUNITY_ASSESSMENT:
            st.button("Previous", on_click=previous_step)
    with col2:
        if st.session_state.current_step != Step.RESULT:
            st.button("Next", on_click=next_step)

# Step 1: Initial Opportunity Assessment
def render_opportunity_assessment():
    st.title("Opportunity Assessment")
    st.session_state.responses['v3_vertical'] = st.radio(
        "Is the project supported in V3 verticals?",
        ('Yes', 'No')
    )

# Step 2: V3 Qualification Process
def render_v3_qualification():
    st.title("V3 Qualification")
    st.session_state.responses['v3_vertical_type'] = st.selectbox(
        "Select Supported Vertical", 
        ["Smart Buildings", "Asset Management", "Utilities", "Cold Chain Monitoring", "Waste Management"]
    )

# Step 3: Smart Buildings Qualification
def render_smart_buildings():
    st.title("Smart Buildings Qualification")
    st.session_state.responses['bms_hvac'] = st.radio(
        "Does the project involve BMS/HVAC integration?",
        ('Yes', 'No')
    )
    if st.session_state.responses['bms_hvac'] == 'No':
        st.session_state.responses['occupancy_tracking'] = st.radio(
            "Does the project involve occupancy tracking?",
            ('Yes', 'No')
        )
        if st.session_state.responses['occupancy_tracking'] == 'Yes':
            st.session_state.responses['camera_based'] = st.radio(
                "Is the project using cameras for occupancy tracking?",
                ('Yes', 'No')
            )
            if st.session_state.responses['camera_based'] == 'Yes':
                st.session_state.responses['camera_accuracy'] = st.radio(
                    "Does the camera have 99% accuracy?",
                    ('Yes', 'No')
                )
                if st.session_state.responses['camera_accuracy'] == 'No':
                    st.write("Recommend using 3D Milesight sensors.")
            else:
                st.write("Proceed with standard occupancy tracking.")
        else:
            st.write("Proceed with BMS/HVAC control.")

# Step 4: Asset Management
def render_asset_management():
    st.title("Asset Management Qualification")
    st.session_state.responses['asset_management'] = st.radio(
        "Does the project require asset management (predictive maintenance, asset utilization)?",
        ('Yes', 'No')
    )
    if st.session_state.responses['asset_management'] == 'Yes':
        st.session_state.responses['asset_telemetry'] = st.radio(
            "Does the project require telemetry below 15-minute intervals?",
            ('Yes', 'No')
        )
        if st.session_state.responses['asset_telemetry'] == 'Yes':
            st.write("Decline Project: Cannot support real-time telemetry.")
        else:
            st.write("Proceed with asset management support.")

# Step 5: Cold Chain Monitoring
def render_cold_chain():
    st.title("Cold Chain Monitoring")
    st.session_state.responses['cold_chain'] = st.radio(
        "Does the project involve cold chain monitoring?",
        ('Yes', 'No')
    )
    if st.session_state.responses['cold_chain'] == 'Yes':
        st.write("Proceed with cold chain monitoring support.")
    else:
        st.write("Decline Project.")

# Step 6: Waste Management
def render_waste_management():
    st.title("Waste Management")
    st.session_state.responses['waste_management'] = st.radio(
        "Does the project involve waste bin monitoring?",
        ('Yes', 'No')
    )
    if st.session_state.responses['waste_management'] == 'Yes':
        st.session_state.responses['waste_bins'] = st.radio(
            "Does the project involve between 1000 and 10000 waste bins?",
            ('Yes', 'No')
        )
        if st.session_state.responses['waste_bins'] == 'Yes':
            st.write("Proceed with waste bin monitoring support.")
        else:
            st.write("Decline Project.")

# Step 7: V5 Qualification
def render_v5_qualification():
    st.title("V5 Qualification")
    st.session_state.responses['v5_customization'] = st.radio(
        "Does the project require customization?",
        ('Yes', 'No')
    )
    if st.session_state.responses['v5_customization'] == 'Yes':
        st.write("Proceed with Bespoke solution.")
    else:
        st.session_state.responses['v5_roadmap'] = st.radio(
            "Is the project aligned with the product roadmap for V5?",
            ('Yes', 'No')
        )
        if st.session_state.responses['v5_roadmap'] == 'Yes':
            st.write("Proceed with V5 product.")
        else:
            st.write("Check if it fits within Platform solution.")

# Step 8: Bespoke Solution Qualification
def render_bespoke_qualification():
    st.title("Bespoke Solution Qualification")
    st.session_state.responses['bespoke_complexity'] = st.radio(
        "What is the technical complexity of the project?",
        ('Low', 'High')
    )
    if st.session_state.responses['bespoke_complexity'] == 'High':
        st.write("Proceed with Bespoke solution.")
    else:
        st.write("Proceed with Platform/Product.")

# Step 9: Financial Feasibility
def render_financial_feasibility():
    st.title("Financial Feasibility")
    st.session_state.responses['budget'] = st.radio(
        "Does the project have a clear budget and ROI within 2-3 years?",
        ('Yes', 'No')
    )
    st.session_state.responses['strategic_value'] = st.radio(
        "Is there long-term strategic value?",
        ('Yes', 'No')
    )
    if st.session_state.responses['budget'] == 'Yes' and st.session_state.responses['strategic_value'] == 'Yes':
        st.write("Proceed with the deal.")
    else:
        st.write("Decline Project.")

# Step 10: Final Result
def render_final_result():
    st.title("Final Decision")
    st.write("Final Decision: Based on your input, the project classification is complete.")
    st.write(st.session_state.responses)  # Show summary of all responses

# Main Application Flow
def main():
    st.sidebar.title("Deal Qualification Wizard")
    
    # Display current step
    st.sidebar.write(f"Current step: {st.session_state.current_step.name}")
    
    # Render appropriate UI for each step
    if st.session_state.current_step == Step.OPPORTUNITY_ASSESSMENT:
        render_opportunity_assessment()
    elif st.session_state.current_step == Step.V3_QUALIFICATION:
        render_v3_qualification()
    elif st.session_state.current_step == Step.SMART_BUILDINGS:
        render_smart_buildings()
    elif st.session_state.current_step == Step.ASSET_MANAGEMENT:
        render_asset_management()
    elif st.session_state.current_step == Step.COLD_CHAIN:
        render_cold_chain()
    elif st.session_state.current_step == Step.WASTE_MANAGEMENT:
        render_waste_management()
    elif st.session_state.current_step == Step.V5_QUALIFICATION:
        render_v5_qualification()
    elif st.session_state.current_step == Step.BESPOKE_QUALIFICATION:
        render_bespoke_qualification()
    elif st.session_state.current_step == Step.FINANCIAL_FEASIBILITY:
        render_financial_feasibility()
    elif st.session_state.current_step == Step.RESULT:
        render_final_result()

    render_navigation()

if __name__ == "__main__":
    main()
