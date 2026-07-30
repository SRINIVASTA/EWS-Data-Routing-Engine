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

# Sidebar Configuration - Updated to 3 modes
st.sidebar.header("System Controls")
app_mode = st.sidebar.radio(
    "Select View Mode", 
    ["Single Applicant Audit", "1,000 Profile Database Analytics", "Upload Application File (.CSV)"]
)

# ----------------------------------------------------
# MODE 1: SINGLE APPLICANT AUDIT
# ----------------------------------------------------
if app_mode == "Single Applicant Audit":
    st.header("👤 Real-Time Live Application Telemetry")
    tier_input = st.sidebar.selectbox("Applicant Geo Pincode Classification", ['Tier-1', 'Tier-2', 'Tier-3'])
    simulate_btn = st.sidebar.button("Fetch Live Registry Data Pipeline")

    if simulate_btn:
        raw_payload = generate_synthetic_profile(tier_input)
        evaluation = engine.evaluate_applicant(raw_payload, tier_input)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Decoupled Registry Payloads Received")
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

        metrics_df = pd.DataFrame({
            "Metrics": ["Reported Income", "UPI Volume", "Lifestyle Spending Metrics"],
            "Value (INR)": [raw_payload['Reported_Income_INR'], raw_payload['UPI_Transaction_Volume_INR'], raw_payload['Annual_Utility_Bills_INR']]
        })
        fig = px.bar(metrics_df, x='Metrics', y='Value (INR)', title="Financial Discrepancy Multiplier Graph")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💡 Select geometric parameters on the sidebar and click 'Fetch Live Registry Data Pipeline' to test system telemetry.")

# ----------------------------------------------------
# MODE 2: 1,000 PROFILE DATABASE ANALYTICS
# ----------------------------------------------------
elif app_mode == "1,000 Profile Database Analytics":
    st.header("📈 1,000 Profile Database Distribution Analytics")
    st.write("Processing simulated cross-registry batch dataset to map risk patterns and flag potential evasion trends.")
    
    if 'bulk_data' not in st.session_state:
        with st.spinner("Generating 1,000 synthetic database profiles..."):
            st.session_state.bulk_data = generate_bulk_dataset(1000)
            
            eval_results = []
            for _, row in st.session_state.bulk_data.iterrows():
                eval_res = engine.evaluate_applicant(row, row['Pincode_Tier'])
                eval_results.append(eval_res)
                
            eval_df = pd.DataFrame(eval_results)
            st.session_state.bulk_data = pd.concat([st.session_state.bulk_data, eval_df], axis=1)

    df = st.session_state.bulk_data

    # Main Metrics Bar
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Applications Evaluated", f"{len(df)} Rows")
    m2.metric("Passed Verification Clearances (In EWS)", f"{len(df[df['Status'] == 'ELIGIBLE'])} Rows")
    m3.metric("Flagged for Audit (Above EWS / Fraud Risk)", f"{len(df[df['Status'] != 'ELIGIBLE'])} Rows")

    # Interactive Dashboard Charts
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig1 = px.histogram(df, x="True_Segment", color="Status", barmode="group",
                            title="System Decision Accuracy vs True Profile Persona",
                            color_discrete_map={"ELIGIBLE": "#2ecc71", "MANUAL_REVIEW_REQUIRED": "#f1c40f", "FLAGGED_FOR_AUDIT": "#e74c3c"})
        st.plotly_chart(fig1, use_container_width=True)

    with col_chart2:
        fig2 = px.scatter(df, x="Reported_Income_INR", y="UPI_Transaction_Volume_INR", color="Status",
                          size="Annual_Utility_Bills_INR", hover_data=["Applicant_ID"],
                          title="Anomaly Detection: Reported Income vs UPI Velocity Profile",
                          color_discrete_map={"ELIGIBLE": "#2ecc71", "MANUAL_REVIEW_REQUIRED": "#f1c40f", "FLAGGED_FOR_AUDIT": "#e74c3c"})
        st.plotly_chart(fig2, use_container_width=True)

    # Database Segmentation Tabs
    st.subheader("📋 Registry Database Classification System")
    ews_approved_df = df[df['Status'] == 'ELIGIBLE']
    above_ews_df = df[df['Status'].isin(['FLAGGED_FOR_AUDIT', 'MANUAL_REVIEW_REQUIRED'])]

    tab1, tab2, tab3 = st.tabs([
        f"🌐 Full Master Database ({len(df)} Rows)",
        f"✅ Approved EWS Beneficiaries ({len(ews_approved_df)} Rows)", 
        f"🚫 Above EWS Threshold / Flagged ({len(above_ews_df)} Rows)"
    ])
    
    with tab1:
        csv_full = df.drop(columns=['True_Segment']).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Full Master Database (CSV)", csv_full, "full_master_database.csv", "text/csv")
        st.dataframe(df.drop(columns=['True_Segment']), use_container_width=True)
    with tab2:
        csv_eligible = ews_approved_df.drop(columns=['True_Segment']).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Approved EWS List (CSV)", csv_eligible, "approved_ews_beneficiaries.csv", "text/csv")
        st.dataframe(ews_approved_df.drop(columns=['True_Segment']), use_container_width=True)
    with tab3:
        csv_flagged = above_ews_df.drop(columns=['True_Segment']).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Above EWS List (CSV)", csv_flagged, "above_ews_flagged_list.csv", "text/csv")
        st.dataframe(above_ews_df.drop(columns=['True_Segment']), use_container_width=True)

# ----------------------------------------------------
# MODE 3: UPLOAD APPLICATION FILE (.CSV)
# ----------------------------------------------------
else:
    st.header("📤 Custom File Batch Processing Portal")
    st.write("Upload a custom `.csv` applicant batch table to check records against cross-registry validation logic.")
    
    # Template instruction guide for the administrator
    with st.expander("🛠️ View Required CSV Column Schema Guidelines"):
        st.code(
            "Applicant_ID, Reported_Income_INR, UPI_Transaction_Volume_INR, "
            "Annual_Utility_Bills_INR, Nuclear_Property_SqFt, Grandfather_Land_Acres, "
            "Grandfather_Living_Status, Father_Siblings_Count, Pincode_Tier"
        )
        st.info("💡 Note: You can upload the 'synthetic_ews_registry_data.csv' file generated by mock_data.py to test this feature instantly!")

    uploaded_file = st.sidebar.file_uploader("Upload Applicant Telemetry File", type=["csv"])

    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            
            # Runtime validation execution loop
            eval_results = []
            for _, row in uploaded_df.iterrows():
                # Extract dynamic tier classification safely from column string
                tier = row.get('Pincode_Tier', 'Tier-2')
                eval_res = engine.evaluate_applicant(row, tier)
                eval_results.append(eval_res)
            
            processed_eval_df = pd.DataFrame(eval_results)
            final_uploaded_df = pd.concat([uploaded_df, processed_eval_df], axis=1)
            
            # Operational segmentation filters
            up_ews_approved = final_uploaded_df[final_uploaded_df['Status'] == 'ELIGIBLE']
            up_above_ews = final_uploaded_df[final_uploaded_df['Status'].isin(['FLAGGED_FOR_AUDIT', 'MANUAL_REVIEW_REQUIRED'])]
            
            # Visual Executive Analytics Summary cards
            c1, c2, c3 = st.columns(3)
            c1.metric("Uploaded Records Found", f"{len(final_uploaded_df)} Rows")
            c2.metric("Verified Valid Quota Profiles (In EWS)", f"{len(up_ews_approved)} Rows")
            c3.metric("High-Risk Outliers Found (Above EWS)", f"{len(up_above_ews)} Rows")
            
            # Interactive output layout tabs
            utab1, utab2, utab3 = st.tabs([
                f"🌐 Processed Dataset ({len(final_uploaded_df)} Rows)",
                f"✅ Verified EWS Pool ({len(up_ews_approved)} Rows)",
                f"🚫 Flagged/Above EWS Pool ({len(up_above_ews)} Rows)"
            ])
            
            with utab1:
                st.dataframe(final_uploaded_df, use_container_width=True)
            with utab2:
                st.dataframe(up_ews_approved, use_container_width=True)
            with utab3:
                st.dataframe(up_above_ews, use_container_width=True)
                
            st.success("🎉 Batch processing routine executed successfully!")
            
        except Exception as e:
            st.error(f"❌ Structural Parsing Error: Please verify your columns match requirements. Technical details: {e}")
    else:
        st.info("📥 Drag and drop or browse for your `.csv` dataset in the sidebar dashboard module to run evaluations.")
