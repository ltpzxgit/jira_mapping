import streamlit as st
import pandas as pd
from io import BytesIO

st.title("JIRA → LDSO Generator 🚀")

uploaded_file = st.file_uploader("Upload JIRA CSV/XLSX", type=["csv", "xlsx"])

if uploaded_file is not None:

    # ===== READ JIRA =====
    if uploaded_file.name.endswith(".csv"):
        df_jira = pd.read_csv(uploaded_file)
    else:
        df_jira = pd.read_excel(uploaded_file)

    st.success("✅ JIRA Loaded")

    # ===== LOAD TEMPLATE (ต้องอยู่ใน repo) =====
    template_file = "JIRA_LDSO_template.xlsx"
    df_template = pd.read_excel(template_file)

    # 👉 เอา column จาก template เป๊ะๆ
    template_columns = df_template.columns.tolist()

    # ===== CREATE OUTPUT BASE ON TEMPLATE =====
    df_output = pd.DataFrame(columns=template_columns)

    # ===== SYSTEM LOGIC =====
    def map_system(summary):
        if pd.isna(summary):
            return None

        s = summary.upper()

        if 'AZURE' in s:
            return 'TCAP Cloud'
        elif 'L-DCM' in s:
            return 'LDCM'
        else:
            return None

    # ===== MAP DATA =====
    for col in template_columns:

        if col == 'System':
            df_output[col] = df_jira['Summary'].apply(map_system)

        elif col == 'Issue Key' and 'Issue key' in df_jira.columns:
            df_output[col] = df_jira['Issue key']

        elif col in df_jira.columns:
            df_output[col] = df_jira[col]

        else:
            # column ที่ไม่มีใน jira → ปล่อยว่าง
            df_output[col] = None

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
