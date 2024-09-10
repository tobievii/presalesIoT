import streamlit as st

# Supported V3 Verticals and V5 Feature Modules
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

# Wizard to guide users through decision tree
st.set_page_config(page_title="IoT.nxt Deal Qualification Wizard", layout="centered")

st.title("IoT.nxt - Deal Qualification Wizard")

# Step 1: Initial Opportunity Assessment
st.header("Step 1: Initial Opportunity Assessment")
st.write("Identify customer needs and check alignment with existing capabilities (V5, V3).")

aligned_with_capabilities = st.selectbox("Is the project aligned with V5 or V3 capabilities?", ("Yes", "No"))

if aligned_with_capabilities == "No":
    st.write("The project is not aligned with V3 or V5 capabilities. Consider offering a partner-led or bespoke solution.")
    partner_solution = st.button("Offer Partner-Led Solution")
else:
    # Proceed with V3 or V5 qualification
    project_supported = st.selectbox("Is the project supported in V3 verticals?", ("Yes", "No"))

    if project_supported == "No":
        st.write("V3 doesn't support this project. Consider V5, Platform, or Bespoke.")
        next_step = st.button("Go to V5/Platform/Bespoke Assessment")
    else:
        # Let the user choose the supported vertical
        vertical_selection = st.selectbox("Which vertical does the project fall under?", v3_verticals)
        
        devices_catalogue = st.selectbox("Are the required devices in the current V3 device catalogue?", ("Yes", "No"))
        
        if devices_catalogue == "No":
            st.write("Devices are not supported in V3 catalogue. Consider V5/Bespoke solutions.")
            next_step = st.button("Go to V5/Bespoke Assessment")
        else:
            # Question: Frequency for Devices to Send Data/Telemetry
            telemetry_frequency = st.number_input(
                "How many times per day do the devices send telemetry data?", 
                min_value=1, max_value=1440, step=1, value=96  # default is 96/day for V3
            )
            
            # Check if the telemetry frequency fits within the V3 15-minute block constraint
            if telemetry_frequency > 96:
                st.write(f"Telemetry frequency exceeds the V3 15-minute block limit ({telemetry_frequency}/day).")
                st.write("Consider V5/Bespoke for higher or real-time telemetry frequency.")
                next_step = st.button("Go to V5/Bespoke Assessment")
            else:
                st.write(f"The project is supported in V3 under the '{vertical_selection}' vertical and complies with telemetry constraints.")
                next_step = st.button("Proceed with V3 Solution")

# Step 2: Customization Requirement Assessment (If project doesn't fit V3)
if st.session_state.get("next_step"):
    st.header("Step 2: Customization Requirement Assessment")
    customization_required = st.selectbox("Does the project require customization?", ("Yes", "No"))
    
    if customization_required == "Yes":
        st.write("The project requires full customization. Consider Bespoke solution.")
        custom_solution = st.button("Proceed with Bespoke Solution")
    else:
        st.write("Proceed with Solution (Platform).")
        fixed_features = st.selectbox("Are platform/fixed features available for this project?", ("Yes", "No"))
        
        if fixed_features == "Yes":
            st.write("The project fits the Solution (Platform). Proceed with Platform Solution.")
            platform_solution = st.button("Proceed with Platform Solution")
        else:
            # Check for V5 feature module
            st.write("Platform does not support this. Consider Product (V5) or Bespoke.")
            feature_module = st.selectbox("Does the project fit one of the V5 feature modules?", v5_feature_modules)
            
            if feature_module:
                st.write(f"The project fits the V5 feature module '{feature_module}'. Proceed with V5 Product Solution.")
                product_solution = st.button("Proceed with Product (V5)")
            else:
                st.write("Requires full customization. Consider Bespoke solution.")
                bespoke_solution = st.button("Proceed with Bespoke Solution")

# Step 3: Technical Fit Assessment
if st.session_state.get("product_solution") or st.session_state.get("bespoke_solution"):
    st.header("Step 3: Technical Fit Assessment")
    technical_complexity = st.selectbox("What is the technical complexity of the project?", ("Low", "High"))
    
    if technical_complexity == "Low":
        st.write("Low complexity, proceed with Platform/Product solution.")
        technical_fit = st.button("Proceed with Technical Fit")
    else:
        st.write("High complexity, bespoke deployment required.")
        bespoke_technical_fit = st.button("Proceed with Bespoke Technical Fit")

# Step 4: Financial Feasibility
if st.session_state.get("technical_fit") or st.session_state.get("bespoke_technical_fit"):
    st.header("Step 4: Financial Feasibility")
    budget = st.selectbox("Does the customer have a clear budget?", ("Yes", "No"))
    
    if budget == "No":
        st.write("Customer has no clear budget. Defer project or recommend partner solution.")
        defer_project = st.button("Defer Project or Recommend Partner")
    else:
        roi = st.selectbox("Is there a clear ROI within 2-3 years?", ("Yes", "No"))
        
        if roi == "No":
            st.write("Project ROI is not clear. Defer project.")
            defer_roi_project = st.button("Defer Project")
        else:
            st.write("Proceed with the deal based on ROI and Budget.")
            proceed_deal = st.button("Proceed with Deal")

# Step 5: Proceed Decision
if st.session_state.get("proceed_deal"):
    st.header("Final Step: Proceed Decision")
    st.write("Congratulations! Based on your answers, you can proceed with the selected solution.")
    st.write("If further evaluation is required, consider revisiting the customization or financial aspects.")
    st.button("Complete the Wizard")

