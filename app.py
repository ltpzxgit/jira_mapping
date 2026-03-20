import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Transform Tool", layout="wide")

st.title("📊 Excel Transform Tool (Auto Generate Columns)")

uploaded_file = st.file_uploader("Upload your raw data file", type=["csv", "xlsx"])

def transform_data(df):
    # ====== ตัวอย่าง logic (แก้ได้ตามจริง) ======
    
    # สมมติ raw มี column ชื่อ Description
    # แล้วเราจะ parse ข้อมูลออกมา
    
    df['System'] = df['Description'].str.extract(r'(FDF|L-DCM|ABC)', expand=False)
    
    df['Change'] = df['Description'].apply(
        lambda x: "Update" if "update" in str(x).lower() else "Create"
    )
    
    df['Error Name'] = df['Description'].apply(
        lambda x: "Timeout" if "timeout" in str(x).lower() else "Unknown"
    )
    
    df['Service name'] = df['Description'].apply(
        lambda x: "Vehicle API" if "vehicle" in str(x).lower() else "General Service"
    )
    
    df['Service Cat.'] = df['Service name'].apply(
        lambda x: "Core" if "Vehicle" in x else "Support"
    )

    # เลือกเฉพาะ columns ที่ต้องการ
    output = df[['System', 'Change', 'Error Name', 'Service name', 'Service Cat.']]

    return output

if uploaded_file:
    try:
        # อ่านไฟล์
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📥 Raw Data")
        st.dataframe(df)

        # Transform
        result_df = transform_data(df)

        st.subheader("✅ Transformed Data")
        st.dataframe(result_df)

        # Download
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Result",
            data=csv,
            file_name="transformed_data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")
