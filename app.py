import streamlit as st
import pandas as pd

st.set_page_config(page_title="ITOSE Tools", layout="wide")

st.title("Tools Service Mapping")

raw_file = st.file_uploader("Upload Jira", type=["csv", "xlsx"])
example_file = st.file_uploader("Upload Template", type=["csv", "xlsx"])

def read_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if raw_file and example_file:
    try:
        df_raw = read_file(raw_file)
        df_example = read_file(example_file)

        st.subheader("Jira Data")
        st.dataframe(df_raw.head())

        # 👇 เลือก column ที่จะใช้แทน D2 (กันพลาด)
        selected_col = st.selectbox("📌 เลือก column สำหรับใช้ parse (แทน D2)", df_raw.columns)

        # 👉 เอา column จาก example เป็น master
        target_columns = list(df_example.columns)

        st.subheader("📌 Target Columns")
        st.write(target_columns)

        result_df = pd.DataFrame()

        for col in target_columns:

            # =========================
            # 🔥 System
            # =========================
            if col == "System":
                result_df[col] = df_raw[selected_col].apply(
                    lambda x: "TCAP Cloud" if "azure" in str(x).lower() else "LDCM"
                )

            # =========================
            # 🔥 Error Name
            # =========================
            elif col == "Error Name":
                error_list = [
                    "E_000_017",
                    "E_000_024",
                    "E_040_001",
                    "E_LDCM_ACT_009",
                    "E_LDCM_ACT_011",
                    "E_LDCM_ACT_021"
                ]

                def find_error(text):
                    text = str(text)
                    for err in error_list:
                        if err.lower() in text.lower():
                            return err
                    return ""

                result_df[col] = df_raw[selected_col].apply(find_error)

            # =========================
            # 🔥 Service name
            # =========================
            elif col == "Service name":
                service_list = [
                    "FDF Linkage",
                    "fdftcaplinkage",
                    "mb_accident_sending",
                    "precnv_bigdata_periodic",
                    "precnv_general_service",
                    "precnv_ig_off",
                    "ProvisioningResponder",
                    "send_message",
                    "B2B Linkage",
                    "B2C Linkage",
                    "dealer_at_ig_off",
                    "dealer_device_abnormal",
                    "drive_data_send",
                    "external_ig_off",
                    "external_mb_device_abnormal",
                    "svt_confirmation_access_monitoring",
                    "tcap_area_crossing_sending",
                    "tcap_ig_off_sending",
                    "tcap_periodic_sending",
                    "tcap_svt_timeout",
                    "tcap_uvun_ig_off_sending",
                    "tcap_uvun_ig_on_sending",
                    "vehicledeliverytcaplinkage",
                    "VehicleDeliveryTCAPLinkageVin",
                    "vehiclesettingrequester"
                ]

                def find_service(text):
                    text = str(text)
                    for svc in service_list:
                        if svc.lower() in text.lower():
                            return svc
                    return ""

                result_df[col] = df_raw[selected_col].apply(find_service)

            # =========================
            # 🧾 Column อื่น
            # =========================
            else:
                if col in df_raw.columns:
                    result_df[col] = df_raw[col]
                else:
                    result_df[col] = ""

        st.subheader("✅ Result (Template + Auto Logic)")
        st.dataframe(result_df.head())

        # Download
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Result",
            data=csv,
            file_name="service mapping.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")
