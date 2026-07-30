import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from mock_data import generate_synthetic_profile, generate_bulk_dataset
from engine import EWSDecisionEngine

st.set_page_config(page_title="National EWS Data Routing Engine", layout="wide")

st.title("🛡️ Automated National EWS Welfare & Quota Routing Engine")
st.write("Real-time zero-knowledge verification framework leveraging cross-registry telemetry.")

# Initialize Engine
engine = EWSDecisionEngine()

# Helper function to generate PDF certificate on the fly
def generate_pdf_certificate(row):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, leading=24, textColor=colors.HexColor('#1A365D'), alignment=1)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor('#4A5568'), alignment=1)
    section_heading = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontSize=14, leading=18, textColor=colors.HexColor('#2B6CB0'), spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=11, leading=16, textColor=colors.HexColor('#2D3748'))
    
    # Header Elements
    story.append(Paragraph("GOVERNMENT OF INDIA", title_style))
    story.append(Paragraph("NATIONAL EWS VERIFICATION & DATA ROUTING AUTHORITY", subtitle_style))
    story.append(Spacer(1, 15))
    
    # Status Flag Box styling
    status = str(row['Status'])
    status_color = '#2ECC71' if status == 'ELIGIBLE' else '#F1C40F' if status == 'MANUAL_REVIEW_REQUIRED' else '#E74C3C'
    status_text = f"<font color='{status_color}'><b>{status}</b></font>"
    
    story.append(Paragraph("INCOME & ASSET VERIFICATION REPORT", section_heading))
    story.append(Spacer(1, 5))
    
    # Key Value Array Setup
    data = [
        [Paragraph("<b>Applicant Unique ID:</b>", body_style), Paragraph(str(row['Applicant_ID']), body_style)],
        [Paragraph("<b>Verification System Status:</b>", body_style), Paragraph(status_text, body_style)],
        [Paragraph("<b>Risk System Assessment Score:</b>", body_style), Paragraph(f"{row['Risk_Score']}%", body_style)],
        [Paragraph("<b>Reported Gross Income (Annual):</b>", body_style), Paragraph(f"INR {row['Reported_Income_INR']:,.2f}", body_style)],
        [Paragraph("<b>UPI Transaction Volume (12 Mo):</b>", body_style), Paragraph(f"INR {row['UPI_Transaction_Volume_INR']:,.2f}", body_style)],
        [Paragraph("<b>Annual Utility Footprint:</b>", body_style), Paragraph(f"INR {row['Annual_Utility_Bills_INR']:,.2f}", body_style)],
        [Paragraph("<b>Total Evaluated Farmland:</b>", body_style), Paragraph(f"{row['Effective_Land_Acres']} Acres", body_style)],
        [Paragraph("<b>Geographic Classification:</b>", body_style), Paragraph(str(row['Pincode_Tier']), body_style)]
    ]
    
    t = Table(data, colWidths=[200, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)
    
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>Disclaimer:</b> This document is a computer-generated cryptographic verification report synthesized directly via real-time database endpoints. No manual physical signatures are required.", subtitle_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Sidebar Configuration - 3 modes
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
            st.metric("Total Land Holding (Inc. Ancestral Farmland)", f"{evaluation['Effective_Land_Acres']} Acres")
            st.metric("PPP Adjusted Income Limit", f"₹ {evaluation['Adjusted_Income_Threshold']:,.2f}")

        if evaluation['Effective_Land_Acres'] > 5.0:
            st.error(f"⚠️ LAND BREACH DETECTED: This applicant possesses {evaluation['Effective_Land_Acres']} acres of total land, exceeding the statutory 5-acre agricultural cap.")

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
                tier = row.get('Pincode_Tier', 'Tier-2')
                eval_res = engine.evaluate_applicant(row, tier)
                eval_results.append(eval_res)
                
            eval_df = pd.DataFrame(eval_results)
            st.session_state.bulk_data = pd.concat([st.session_state.bulk_data, eval_df], axis=1)

    df = st.session_state.bulk_data

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Evaluated", f"{len(df)} Rows")
    m2.metric("Passed In EWS", f"{len(df[df['Status'] == 'ELIGIBLE'])} Rows")
    m3.metric("Above EWS / Flagged", f"{len(df[df['Status'] != 'ELIGIBLE'])} Rows")
    land_breaches = len(df[df['Effective_Land_Acres'] > 5.0])
    m4.metric("Farmland Cap Breaches (>5 Acres)", f"{land_breaches} Rows", delta="-Critical Indicator", delta_color="inverse")

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig1 = px.histogram(df, x="True_Segment", color="Status", barmode="group",
                            title="System Decision Accuracy vs True Profile Persona",
                            color_discrete_map={"ELIGIBLE": "#2ecc71", "MANUAL_REVIEW_REQUIRED": "#f1c40f", "FLAGGED_FOR_AUDIT": "#e74c3c"})
        st.plotly_chart(fig1, use_container_width=True)

    with col_chart2:
        fig2 = px.scatter(df, x="Reported_Income_INR", y="Effective_Land_Acres", color="Status",
                          size="Grandfather_Land_Acres", hover_data=["Applicant_ID"],
                          title="Land Ownership Scatter: Reported Income vs Total Effective Land Acres",
                          color_discrete_map={"ELIGIBLE": "#2ecc71", "MANUAL_REVIEW_REQUIRED": "#f1c40f", "FLAGGED_FOR_AUDIT": "#e74c3c"})
        fig2.add_hline(y=5.0, line_dash="dash", line_color="red", annotation_text="Legal 5-Acre Limit")
        st.plotly_chart(fig2, use_container_width=True)

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
# MODE 3: UPLOAD APPLICATION FILE (.CSV) - WITH PLOTLY & PDF
# ----------------------------------------------------
else:
    st.header("📤 Custom File Batch Processing Portal")
    st.write("Upload a custom `.csv` applicant batch table to check records against cross-registry validation logic.")
    
    with st.expander("🛠️ View Required CSV Column Schema Guidelines"):
        st.code(
            "Applicant_ID, Reported_Income_INR, UPI_Transaction_Volume_INR, "
            "Annual_Utility_Bills_INR, Nuclear_Property_SqFt, Grandfather_Land_Acres, "
            "Grandfather_Living_Status, Father_Siblings_Count, Pincode_Tier"
        )
        st.info("ℹ️ The platform processes the 'Grandfather_Land_Acres' field dynamically using systemic inheritance rules to verify agricultural land limits.")

    uploaded_file = st.sidebar.file_uploader("Upload Applicant Telemetry File", type=["csv"])

    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            
            # Process uploaded data through engine logic
            eval_results = []
            for _, row in uploaded_df.iterrows():
                tier = row.get('Pincode_Tier', 'Tier-2')
                eval_res = engine.evaluate_applicant(row, tier)
                eval_results.append(eval_res)
            
            processed_eval_df = pd.DataFrame(eval_results)
            final_uploaded_df = pd.concat([uploaded_df, processed_eval_df], axis=1)
            
            up_ews_approved = final_uploaded_df[final_uploaded_df['Status'] == 'ELIGIBLE']
            up_above_ews = final_uploaded_df[final_uploaded_df['Status'].isin(['FLAGGED_FOR_AUDIT', 'MANUAL_REVIEW_REQUIRED'])]
            uploaded_land_breaches = len(final_uploaded_df[final_uploaded_df['Effective_Land_Acres'] > 5.0])
            
            # Metric Summary Bar
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Uploaded Records", f"{len(final_uploaded_df)} Rows")
            c2.metric("Verified Valid Pool (In EWS)", f"{len(up_ews_approved)} Rows")
            c3.metric("High-Risk Outliers (Above EWS)", f"{len(up_above_ews)} Rows")
            c4.metric("Land Threshold Violations", f"{uploaded_land_breaches} Rows")
            
            # --- PDF REPORT CERTIFICATE ACTION TOOL BLOCK ---
            st.subheader("🔏 On-Demand EWS Certificate Generator")
            col_pdf1, col_pdf2 = st.columns(2)
            
            with col_pdf1:
                target_id = st.selectbox("Select Target Applicant ID", final_uploaded_df['Applicant_ID'].unique())
            with col_pdf2:
                target_row = final_uploaded_df[final_uploaded_df['Applicant_ID'] == target_id].iloc[0]
                pdf_data = generate_pdf_certificate(target_row)
                
                st.write("") 
                st.write("")
                st.download_button(
                    label=f"📄 Download Certificate for {target_id} (PDF)",
                    data=pdf_data,
                    file_name=f"EWS_Certificate_{target_id}.pdf",
                    mime="application/pdf"
                )
            # -------------------------------------------------

            # Analytics Charts for Uploaded File
            st.subheader("📊 Analytics Charts for Uploaded File")
            col_up1, col_up2 = st.columns(2)
            
            with col_up1:
                fig_up1 = px.pie(final_uploaded_df, names="Status", 
                                 title="Status Segmentation Breakdown",
                                 color="Status",
                                 color_discrete_map={"ELIGIBLE": "#2ecc71", "MANUAL_REVIEW_REQUIRED": "#f1c40f", "FLAGGED_FOR_AUDIT": "#e74c3c"})
                st.plotly_chart(fig_up1, use_container_width=True)
                
            with col_up2:
                fig_up2 = px.scatter(final_uploaded_df, x="Reported_Income_INR", y="Effective_Land_Acres", 
                                     color="Status", hover_data=["Applicant_ID"],
                                     title="Uploaded Data: Reported Income vs Total Effective Land Acres",
                                     labels={"Reported_Income_INR": "Self-Reported Income", "Effective_Land_Acres": "Calculated Total Acres"},
                                     color_discrete_map={"ELIGIBLE": "#2ecc71", "MANUAL_REVIEW_REQUIRED": "#f1c40f", "FLAGGED_FOR_AUDIT": "#e74c3c"})
                fig_up2.add_hline(y=5.0, line_dash="dash", line_color="red", annotation_text="Legal 5-Acre Limit")
                st.plotly_chart(fig_up2, use_container_width=True)

            # Interactive output layout tabs
            st.subheader("📋 Uploaded File Segmentation Logs")
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
                
            st.success("🎉 Batch processing routine and visualizations generated successfully!")
            
        except Exception as e:
            st.error(f"❌ Structural Parsing Error: Please verify your columns match requirements. Technical details: {e}")
    else:
        st.info("📥 Drag and drop or browse for your `.csv` dataset in the sidebar dashboard module to run evaluations.")
