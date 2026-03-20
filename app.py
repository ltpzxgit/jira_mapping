import streamlit as st
import pandas as pd

st.set_page_config(page_title="Column Standardizer", layout="wide")

st.title("📊 Excel Column Standardizer (Force Template Columns)")

raw_file = st.file_uploader("📥 Upload RAW data", type=["csv", "xlsx"])
example_file = st.file_uploader("📌 Upload Example (Template)", type=["csv", "xlsx"])

def read_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if raw_file and example_file:
    try:
        df_raw = read_file(raw_file)
        df_example = read_file(example_file)

        st.subheader("📥 Raw Data")
        st.dataframe(df_raw.head())

        # 👉 เอา column จาก example เป็น master
        target_columns = list(df_example.columns)

        st.subheader("📌 Target Columns")
        st.write(target_columns)

        # 🔥 สร้าง DataFrame ใหม่ตาม schema
        result_df = pd.DataFrame()

        for col in target_columns:
            if col in df_raw.columns:
                result_df[col] = df_raw[col]
            else:
                # 👈 ถ้าไม่มีใน raw → สร้าง column เปล่า
                result_df[col] = ""

        st.subheader("✅ Result (Standardized Data)")
        st.dataframe(result_df.head())

        # Download
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Result",
            data=csv,
            file_name="standardized_data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")
