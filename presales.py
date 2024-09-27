import streamlit as st

# Enum for each step in the wizard
class Step:
    OPPORTUNITY_ASSESSMENT = "Opportunity Assessment"
    V3_QUALIFICATION = "V3 Qualification"
    SMART_BUILDINGS = "Smart Buildings"
    ASSET_MANAGEMENT = "Asset Management"
    COLD_CHAIN = "Cold Chain Monitoring"
    WASTE_MANAGEMENT = "Waste Management"
    V5_QUALIFICATION = "V5 Qualification"
    BESPOKE_QUALIFICATION = "Bespoke Qualification"
    FINANCIAL_FEASIBILITY = "Financial Feasibility"
    RESULT = "Result"

# Initialize session state for navigation and responses
if 'current_step' not in st.session_state:
    st.session_state.current_step = Step.OPPORTUNITY_ASSESSMENT

def next_step():
    if st.session_state.current_step == Step.OPPORTUNITY_ASSESSMENT:
        if st.session_state.v3_supported == 'Yes':
            st.session_state.current_step = Step.V3_QUALIFICATION
        else:
            st.session_state.current_step = Step.V5_QUALIFICATION
    elif st.session_state.current_step == Step.V3_QUALIFICATION:
        if st.session_state.v3_vertical == "Smart Buildings":
            st.session_state.current_step = Step.SMART_BUILDINGS
        elif st.session_state.v3_vertical == "Asset Management":
            st.session_state.current_step = Step.ASSET_MANAGEMENT
        elif st.session_state.v3_vertical == "Cold Chain Monitoring":
            st.session_state.current_step = Step.COLD_CHAIN
        elif st.session_state.v3_vertical == "Waste Management":
            st.session_state.current_step = Step.WASTE_MANAGEMENT
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

def previous_step():
    if st.session_state.current_step == Step.V3_QUALIFICATION:
        st.session_state.current_step = Step.OPPORTUNITY_ASSESSMENT
    elif st.session_state.current_step in [
        Step.SMART_BUILDINGS, Step.ASSET_MANAGEMENT, Step.COLD_CHAIN, Step.WASTE_MANAGEMENT]:
        st.session_state.current_step = Step.V3_QUALIFICATION
    elif st.session_state.current_step == Step.V5_QUALIFICATION:
        st.session_state.current_step = Step.OPPORTUNITY_ASSESSMENT
    elif st.session_state.current_step == Step.BESPOKE_QUALIFICATION:
        st.session_state.current_step = Step.V5_QUALIFICATION
    elif st.session_state.current_step == Step.FINANCIAL_FEASIBILITY:
        st.session_state.current_step = Step.BESPOKE_QUALIFICATION

# Render the opportunity assessment step
def render_opportunity_assessment():
    st.title("Opportunity Assessment")
    st.session_state.v3_supported = st.radio(
        "Is the project supported in V3 verticals?",
        ('Yes', 'No')
    )
    st.button("Next", on_click=next_step)

# Render the V3 Qualification Step
def render_v3_qualification():
    st.title("V3 Qualification")
    st.session_state.v3_vertical = st.selectbox(
        "Select Supported Vertical", 
        ["Smart Buildings", "Asset Management", "Utilities", "Cold Chain Monitoring", "Waste Management"]
    )
    st.button("Next", on_click=next_step)
    st.button("Previous", on_click=previous_step)

# Render the Smart Buildings qualification step
def render_smart_buildings():
    st.title("Smart Buildings Qualification")
    st.session_state.bms_hvac = st.radio(
        "Does the project involve BMS/HVAC integration?",
        ('Yes', 'No')
    )
    st.button("Next", on_click=next_step)
    st.button("Previous", on_click=previous_step)

# Render the Asset Management qualification step
def render_asset_management():
    st.title("Asset Management Qualification")
    st.session_state.asset_management = st.radio(
        "Does the project require asset management?",
        ('Yes', 'No')
    )
    st.button("Next", on_click=next_step)
    st.button("Previous", on_click=previous_step)

# Main Application Logic
def main():
    st.sidebar.title("Deal Qualification Wizard")
    current_step = st.session_state.current_step
    st.sidebar.write(f"Current step: {current_step}")

    # Control the flow based on the current step
    if current_step == Step.OPPORTUNITY_ASSESSMENT:
        render_opportunity_assessment()
    elif current_step == Step.V3_QUALIFICATION:
        render_v3_qualification()
    elif current_step == Step.SMART_BUILDINGS:
        render_smart_buildings()
    elif current_step == Step.ASSET_MANAGEMENT:
        render_asset_management()
    # Add other steps here as necessary

if __name__ == "__main__":
    main()
