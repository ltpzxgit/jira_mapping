import streamlit as st
import pandas as pd
from io import BytesIO

st.title("JIRA → LDSO Generator 🚀")

# ===== Upload File =====
uploaded_file = st.file_uploader("Upload JIRA CSV", type=["csv"])

if uploaded_file:
    df_jira = pd.read_csv(uploaded_file)

    st.write("### Preview Data")
    st.dataframe(df_jira.head())

    # ===== Generate Button =====
    if st.button("Generate LDSO File"):
        
        # ===== Mapping =====
        column_mapping = {
            'Issue key': 'Issue Key',
            'Summary': 'Summary',
            'Issue Type': 'Issue Type',
            'Status': 'Status',
            'Priority': 'Priority',
            'Assignee': 'Assignee',
            'Created': 'Created',
            'Updated': 'Updated'
        }

        df_output = df_jira[list(column_mapping.keys())].rename(columns=column_mapping)

        # ===== Create Excel in Memory =====
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_output.to_excel(writer, sheet_name='JIRA_LDSO', index=False)

        output.seek(0)

        # ===== Download Button =====
        st.download_button(
            label="📥 Download LDSO File",
            data=output,
            file_name="JIRA_LDSO_Output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
