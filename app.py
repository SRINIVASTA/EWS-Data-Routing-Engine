import streamlit as st
import pandas as pd
import plotly.express as px
from mock_data import generate_synthetic_profile
from engine import EWSDecisionEngine

st.set_page_config(page_title="National EWS Data Routing Engine", layout="wide")

st.title("🛡️ Automated National EWS Welfare & Quota Routing Engine")
st.write("Real-time zero-knowledge verification framework leveraging cross-registry telemetry.")

# Sidebar Configuration
st.sidebar.header("System Controls")
tier_input = st.sidebar.selectbox("Applicant Geo Pincode Classification", ['Tier-1', 'Tier-2', 'Tier-3'])
simulate_btn = st.sidebar.button("Fetch Live Registry Data Pipeline")

# Initialize Engine
engine = EWSDecisionEngine()

if simulate_btn:
    # 1. Fetch raw payloads from the mock database module
    raw_payload = generate_synthetic_profile(tier_input)
    
    # 2. Process through data science score matrix
    evaluation = engine.evaluate_applicant(raw_payload, tier_input)
    
    # Layout Design
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Decoupled Registry Payloads Recieved")
        st.json(raw_payload)
        
    with col2:
        st.subheader("⚖️ Operational Engine Output")
        
        if evaluation['Status'] == 'ELIGIBLE':
            st.success(f"Status: {evaluation['Status']}")
        elif evaluation['Status'] == 'MANUAL_REVIEW_REQUIRED':
            st.warning(f"Status: {evaluation['Status']}")
        else:
            st.error(f"Status: {evaluation['Status']}")
            
        st.metric("Calculated System Risk Score", f"{evaluation['Risk_Score']}%")
        st.metric("Computed Total Land Holding (Inc. Ancestral Share)", f"{evaluation['Effective_Land_Acres']} Acres")
        st.metric("PPP Adjusted Income Limit for this Location", f"₹ {evaluation['Adjusted_Income_Threshold']:,.2f}")

    # Data Visualization to contextualize risk parameters
    st.subheader("📈 System Anomaly Distribution Map")
    metrics_df = pd.DataFrame({
        "Metrics": ["Reported Income", "UPI Volume", "Lifestyle Spending Metrics"],
        "Value (INR)": [raw_payload['Reported_Income_INR'], raw_payload['UPI_Transaction_Volume_INR'], raw_payload['Annual_Utility_Bills_INR']]
    })
    fig = px.bar(metrics_df, x='Metrics', y='Value (INR)', title="Financial Discrepancy Multiplier Graph")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("💡 Proactively configure the geographic parameters on the sidebar and click 'Fetch Live Registry Data Pipeline' to test system telemetry.")
