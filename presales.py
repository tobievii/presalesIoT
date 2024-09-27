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
    if st.session_state.current_step == Step.OPPORTUNITY_ASSESSMENT:
        if st.session_state.responses.get('v3_vertical') == 'Yes':
            st.session_state.current_step = Step.V3_QUALIFICATION
        else:
            st.session_state.current_step = Step.V5_QUALIFICATION
    elif st.session_state.current_step == Step.V3_QUALIFICATION:
        v3_vertical_type = st.session_state.responses.get('v3_vertical_type')
        if v3_vertical_type in ["Smart Buildings", "Asset Management", "Cold Chain Monitoring", "Waste Management"]:
            if v3_vertical_type == "Smart Buildings":
                st.session_state.current_step = Step.SMART_BUILDINGS
            elif v3_vertical_type == "Asset Management":
                st.session_state.current_step = Step.ASSET_MANAGEMENT
            elif v3_vertical_type == "Cold Chain Monitoring":
                st.session_state.current_step = Step.COLD_CHAIN
            elif v3_vertical_type == "Waste Management":
                st.session_state.current_step = Step.WASTE_MANAGEMENT
        else:
            st.warning("Please select a vertical.")
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
    
    # Add a debug print to ensure this function is being called
    st.write("V3 Qualification: Selecting supported vertical...")
    
    # Ensure that the value exists in the session state, or initialize it
    if 'v3_vertical_type' not in st.session_state.responses:
        st.session_state.responses['v3_vertical_type'] = ""

    # Render the dropdown for vertical selection and store the selected option in session state
    st.session_state.responses['v3_vertical_type'] = st.selectbox(
        "Select Supported Vertical", 
        ["", "Smart Buildings", "Asset Management", "Utilities", "Cold Chain Monitoring", "Waste Management"]
    )

    # Inform user to make a selection if it's empty
    if st.session_state.responses['v3_vertical_type'] == "":
        st.warning("Please select a vertical before proceeding.")

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
    
    # Navigation buttons
    render_navigation()

if __name__ == "__main__":
    main()
