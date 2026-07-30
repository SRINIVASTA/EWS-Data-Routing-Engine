import streamlit as st
import pandas as pd
import plotly.express as px
from mock_data import generate_synthetic_profile, generate_bulk_dataset
from engine import EWSDecisionEngine

st.set_page_config(page_title="National EWS Data Routing Engine", layout="wide")

st.title("🛡️ Automated National EWS Welfare & Quota Routing Engine")
st.write("Real-time zero-knowledge verification framework leveraging cross-registry telemetry.")

# Initialize Engine
engine = EWSDecisionEngine()

# Sidebar Configuration
st.sidebar.header("System Controls")
app_mode = st.sidebar.radio("Select View Mode", ["Single Applicant Audit", "1,000 Profile Database Analytics"])

if app_mode == "Single Applicant Audit":
    st.header("👤 Real-Time Live Application Telemetry")
    tier_input = st.sidebar.selectbox("Applicant Geo Pincode Classification", ['Tier-1', 'Tier-2', 'Tier-3'])
    simulate_btn = st.sidebar.button("Fetch Live Registry Data Pipeline")

    if simulate_btn:
        raw_payload = generate_synthetic_profile(tier_input)
        evaluation = engine.evaluate_applicant(raw_payload, tier_input)
        
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

        # Individual distribution visualization
        metrics_df = pd.DataFrame({
            "Metrics": ["Reported Income", "UPI Volume", "Lifestyle Spending Metrics"],
            "Value (INR)": [raw_payload['Reported_Income_INR'], raw_payload['UPI_Transaction_Volume_INR'], raw_payload['Annual_Utility_Bills_INR']]
        })
        fig = px.bar(metrics_df, x='Metrics', y='Value (INR)', title="Financial Discrepancy Multiplier Graph")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💡 Select geometric parameters on the sidebar and click 'Fetch Live Registry Data Pipeline' to test system telemetry.")

else:
    st.header("📈 1,000 Profile Database Distribution Analytics")
    st.write("Processing simulated cross-registry batch dataset to map risk patterns and flag potential evasion trends.")
    
    # Generate bulk data for batch analysis using st.session_state to avoid losing data on click
    if 'bulk_data' not in st.session_state:
        with st.spinner("Generating 1,000 synthetic database profiles..."):
            st.session_state.bulk_data = generate_bulk_dataset(1000)
            
            # Run engine evaluations on all 1,000 rows
            eval_results = []
            for _, row in st.session_state.bulk_data.iterrows():
                eval_res = engine.evaluate_applicant(row, row['Pincode_Tier'])
                eval_results.append(eval_res)
                
            eval_df = pd.DataFrame(eval_results)
            st.session_state.bulk_data = pd.concat([st.session_state.bulk_data, eval_df], axis=1)

    df = st.session_state.bulk_data

    # Main Executive Metrics Bar
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Applications Evaluated", f"{len(df)} Rows")
    m2.metric("Passed Verification Clearances (In EWS)", f"{len(df[df['Status'] == 'ELIGIBLE'])} Rows")
    m3.metric("Flagged for Audit (Above EWS / Fraud Risk)", f"{len(df[df['Status'] != 'ELIGIBLE'])} Rows")

    # Interactive Dashboard Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig1 = px.histogram(df, x="True_Segment", color="Status", barmode="group",
                            title="System Decision Accuracy vs True Profile Persona",
                            labels={"True_Segment": "Synthetic Profile Demographic Group", "count": "Application Count"},
                            color_discrete_map={"ELIGIBLE": "#2ecc71", "MANUAL_REVIEW_REQUIRED": "#f1c40f", "FLAGGED_FOR_AUDIT": "#e74c3c"})
        st.plotly_chart(fig1, use_container_width=True)

    with col_chart2:
        fig2 = px.scatter(df, x="Reported_Income_INR", y="UPI_Transaction_Volume_INR", color="Status",
                          size="Annual_Utility_Bills_INR", hover_data=["Applicant_ID"],
                          title="Anomaly Detection: Reported Income vs UPI Velocity Profile",
                          labels={"Reported_Income_INR": "Self-Reported Income", "UPI_Transaction_Volume_INR": "True Digital UPI Volume Flows"},
                          color_discrete_map={"ELIGIBLE": "#2ecc71", "MANUAL_REVIEW_REQUIRED": "#f1c40f", "FLAGGED_FOR_AUDIT": "#e74c3c"})
        st.plotly_chart(fig2, use_container_width=True)

    # Database Segmentation View
    st.subheader("📋 Registry Database Classification System")
    
    # Filter the data subsets cleanly
    ews_approved_df = df[df['Status'] == 'ELIGIBLE']
    above_ews_df = df[df['Status'].isin(['FLAGGED_FOR_AUDIT', 'MANUAL_REVIEW_REQUIRED'])]

    # Setup the 3-tab layout interface
    tab1, tab2, tab3 = st.tabs([
        f"🌐 Full Master Database ({len(df)} Rows)",
        f"✅ Approved EWS Beneficiaries ({len(ews_approved_df)} Rows)", 
        f"🚫 Above EWS Threshold / Flagged ({len(above_ews_df)} Rows)"
    ])
    
    with tab1:
        st.write("Complete un-filtered 1,000 row log containing all applicants submitted into the platform.")
        csv_full = df.drop(columns=['True_Segment']).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Full Master Database (CSV)", csv_full, "full_master_database.csv", "text/csv")
        st.dataframe(df.drop(columns=['True_Segment']), use_container_width=True)
        
    with tab2:
        st.write("This list isolates applicants whose cross-registry data matches genuine low-income profiles (In EWS).")
        csv_eligible = ews_approved_df.drop(columns=['True_Segment']).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Approved EWS List (CSV)", csv_eligible, "approved_ews_beneficiaries.csv", "text/csv")
        st.dataframe(ews_approved_df.drop(columns=['True_Segment']), use_container_width=True)
        
    with tab3:
        st.write("This list isolates applicants whose reported income exceeds limits or whose transaction velocities mark them as evaders (Above EWS).")
        csv_flagged = above_ews_df.drop(columns=['True_Segment']).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Above EWS List (CSV)", csv_flagged, "above_ews_flagged_list.csv", "text/csv")
        st.dataframe(above_ews_df.drop(columns=['True_Segment']), use_container_width=True)
