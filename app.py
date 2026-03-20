import streamlit as st
import pandas as pd

st.set_page_config(page_title="Column Filter Tool", layout="wide")

st.title("🧹 Excel Column Filter Tool")

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

        st.subheader("📌 Example Columns")
        st.write(list(df_example.columns))

        # 🔥 เอา columns จาก example
        target_columns = list(df_example.columns)

        # ✅ filter เฉพาะ columns ที่มีอยู่ใน raw
        filtered_columns = [col for col in target_columns if col in df_raw.columns]

        result_df = df_raw[filtered_columns]

        st.subheader("✅ Result (Filtered Data)")
        st.dataframe(result_df.head())

        # Download
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Result",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")
