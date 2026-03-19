import streamlit as st
import pandas as pd
from io import BytesIO

st.title("JIRA → LDSO Generator 🚀")

uploaded_file = st.file_uploader("Upload JIRA file", type=["csv", "xlsx"])

if uploaded_file is not None:

    # ===== AUTO DETECT FILE TYPE =====
    if uploaded_file.name.endswith(".csv"):
        df_jira = pd.read_csv(uploaded_file)
    else:
        df_jira = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded")

    st.dataframe(df_jira.head())

    # ===== GENERATE BUTTON =====
    if st.button("Generate LDSO"):

        # ===== SYSTEM MAPPING =====
        def map_system(summary):
            if pd.isna(summary):
                return None

            s = summary.upper()

            if 'AZURE' in s:
                return 'TCAP Cloud'
            elif 'L-DCM' in s:
                return 'LDCM'
            else:
                return 'Other'

        # ===== CREATE OUTPUT =====
        df_output = pd.DataFrame()

        df_output['Issue Key'] = df_jira['Issue key']
        df_output['Summary'] = df_jira['Summary']
        df_output['System'] = df_jira['Summary'].apply(map_system)
        df_output['Issue Type'] = df_jira['Issue Type']
        df_output['Status'] = df_jira['Status']
        df_output['Priority'] = df_jira['Priority']
        df_output['Assignee'] = df_jira['Assignee']
        df_output['Created'] = pd.to_datetime(df_jira['Created'], errors='coerce')
        df_output['Updated'] = pd.to_datetime(df_jira['Updated'], errors='coerce')

        # ===== EXPORT =====
        output = BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_output.to_excel(writer, sheet_name='JIRA_LDSO', index=False)

        output.seek(0)

        st.download_button(
            label="📥 Download LDSO",
            data=output,
            file_name="JIRA_LDSO_Output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
