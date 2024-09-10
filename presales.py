import streamlit as st

# Supported V3 Verticals, V5 Suites, and V5 Feature Modules
v3_verticals = [
    "Agriculture", "Smart Buildings", "Cold Chain Monitoring", "CCTV Integration",
    "Geo-Fencing", "HVAC Control and Integration", "LPR Cameras", "Personnel Tracking (RFID)",
    "Predictive Maintenance", "Smart Asset Management", "Smart Electric Metering",
    "Smart Workflow", "Threshold Management", "Waste Monitoring/Water Tanks & Tower Monitoring"
]

v5_feature_modules = [
    "Asset Management", "Monitoring & Management", "Event Management",
    "Automation & Control", "Reporting", "AI Analytics", "Maintenance & Dispatch",
    "Documentation Management", "AI Assistant", "Integration Components"
]

v5_suites = ["CSM Suite", "Utilities Suite", "Assets Suite"]

# Set up session state to track the user's path
if 'path' not in st.session_state:
    st.session_state.path = None

# Wizard to guide users through decision tree
st.set_page_config(page_title="IoT.nxt Deal Qualification Wizard", layout="centered")

st.title("IoT.nxt - Deal Qualification Wizard")

# Step 1: Initial Opportunity Assessment
st.header("Step 1: Initial Opportunity Assessment")
st.write("Identify customer needs and check alignment with existing capabilities (V5, V3).")

aligned_with_capabilities = st.selectbox("Is the project aligned with V5 or V3 capabilities?", ("Yes", "No"))

if aligned_with_capabilities == "No":
    st.write("The project is not aligned with V3 or V5 capabilities. Consider offering a partner-led or bespoke solution.")
    if st.button("Offer Partner-Led Solution"):
        st.success("Proceed with a Partner-Led Solution!")
        st.session_state.path = 'partner_solution'
else:
    # Proceed with V3 or V5 qualification
    project_supported = st.selectbox("Is the project supported in V3 verticals?", ("Yes", "No"))

    if project_supported == "No":
        st.write("V3 doesn't support this project. You will now be diverted to the V5/Platform or Bespoke path.")
        if st.button("Proceed with V5/Bespoke Assessment"):
            st.success("Proceeding with V5 or Bespoke Assessment!")
            st.session_state.path = 'v5_bespoke'
    else:
        # Let the user choose the supported vertical
        vertical_selection = st.selectbox("Which vertical does the project fall under?", v3_verticals)
        
        devices_catalogue = st.selectbox("Are the required devices in the current V3 device catalogue?", ("Yes", "No"))
        
        if devices_catalogue == "No":
            st.write("Devices are not supported in V3 catalogue. Consider V5/Bespoke solutions.")
            if st.button("Proceed with V5/Bespoke Assessment"):
                st.success("Proceeding with V5 or Bespoke Assessment!")
                st.session_state.path = 'v5_bespoke'
        else:
            # Question: Frequency for Devices to Send Data/Telemetry
            telemetry_frequency = st.number_input(
                "How many times per day do the devices send telemetry data?", 
                min_value=1, max_value=1440, step=1, value=96  # default is 96/day for V3
            )
            
            # Check if the telemetry frequency fits within the V3 15-minute block constraint
            if telemetry_frequency > 96:
                st.write(f"Telemetry frequency exceeds the V3 15-minute block limit ({telemetry_frequency}/day).")
                st.write("Consider V5 for real-time telemetry support or Bespoke for further customization.")
                if st.button("Proceed with V5/Bespoke Assessment"):
                    st.success("Proceeding with V5 (real-time telemetry support) or Bespoke solution!")
                    st.session_state.path = 'v5_bespoke'
            else:
                st.write(f"The project is supported in V3 under the '{vertical_selection}' vertical and complies with telemetry constraints.")
                if st.button("Proceed with V3 Solution"):
                    st.success(f"Proceeding with V3 Solution in the {vertical_selection} vertical!")
                    st.session_state.path = 'v3_solution'

# V3 Path Handling
if st.session_state.path == 'v3_solution':
    st.header("V3 Solution Path")
    st.write("You are proceeding with the V3 solution. This solution fits your telemetry requirements and supported vertical.")
    st.success("You can complete the project using V3 supported features and capabilities.")

# V5/Bespoke Path Handling
if st.session_state.path == 'v5_bespoke':
    st.header("Step 2: V5 or Bespoke Assessment")

    customization_required = st.selectbox("Does the project require customization or custom deployment?", ("Yes", "No"))
    
    if customization_required == "Yes":
        st.write("The project requires full customization or custom deployment. Proceed with a Bespoke solution.")
        if st.button("Proceed with Bespoke Solution"):
            st.success("Proceeding with Bespoke Solution for custom deployment!")
    else:
        st.write("Proceed with Solution (Platform) or V5 Product.")
        fixed_features = st.selectbox("Are platform/fixed features available for this project?", ("Yes", "No"))
        
        if fixed_features == "Yes":
            st.write("The project fits the Solution (Platform). Proceed with Platform Solution.")
            if st.button("Proceed with Platform Solution"):
                st.success("Proceeding with Platform Solution!")
        else:
            # Check for V5 feature module
            st.write("Platform does not support this. Consider Product (V5) or Bespoke.")
            feature_module = st.selectbox("Does the project fit one of the V5 feature modules?", v5_feature_modules)
            
            if feature_module:
                v5_suite = st.selectbox("Which V5 suite will you use?", v5_suites)
                st.write(f"The project fits the V5 feature module '{feature_module}' and will use the '{v5_suite}' suite.")
                if st.button("Proceed with Product (V5)"):
                    st.success(f"Proceeding with Product (V5) using the {v5_suite} suite!")
            else:
                st.write("Requires full customization. Proceed with Bespoke solution.")
                if st.button("Proceed with Bespoke Solution"):
                    st.success("Proceeding with Bespoke Solution!")

# Step 3: Technical Fit Assessment
if st.session_state.path in ['v5_bespoke', 'product_solution', 'bespoke_solution']:
    st.header("Step 3: Technical Fit Assessment")
    technical_complexity = st.selectbox("What is the technical complexity of the project?", ("Low", "High"))
    
    if technical_complexity == "Low":
        st.write("Low complexity, proceed with Platform/Product solution.")
        if st.button("Proceed with Technical Fit"):
            st.success("Proceeding with Platform/Product technical fit!")
    else:
        st.write("High complexity, bespoke deployment required.")
        if st.button("Proceed with Bespoke Technical Fit"):
            st.success("Proceeding with bespoke technical fit!")

# Step 4: Financial Feasibility
if st.session_state.path in ['technical_fit', 'bespoke_technical_fit']:
    st.header("Step 4: Financial Feasibility")
    budget = st.selectbox("Does the customer have a clear budget?", ("Yes", "No"))
    
    if budget == "No":
        st.write("Customer has no clear budget. Defer project or recommend partner solution.")
        if st.button("Defer Project or Recommend Partner"):
            st.warning("Defer the project or offer partner solution.")
    else:
        roi = st.selectbox("Is there a clear ROI within 2-3 years?", ("Yes", "No"))
        
        if roi == "No":
            st.write("Project ROI is not clear. Defer project.")
            if st.button("Defer Project"):
                st.warning("Project deferred due to unclear ROI.")
        else:
            st.write("Proceed with the deal based on ROI and Budget.")
            if st.button("Proceed with Deal"):
                st.success("Deal approved. Proceed with the solution!")

# Step 5: Proceed Decision
if st.session_state.path == 'proceed_deal':
    st.header("Final Step: Proceed Decision")
    st.write("Congratulations! Based on your answers, you can proceed with the selected solution.")
    st.write("If further evaluation is required, consider revisiting the customization or financial aspects.")
    if st.button("Complete the Wizard"):
        st.balloons()
        st.success("You have completed the wizard and can proceed with the next steps.")
