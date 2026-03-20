import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Auto Transform", layout="wide")

st.title("📊 Auto Generate Columns Tool")

raw_file = st.file_uploader("📥 Upload RAW data", type=["csv", "xlsx"])

def read_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

def generate_columns(df):

    # 👇 สมมติ column D = "Description"
    col = "Description"

    # =========================
    # 🔹 System
    # =========================
    df["System"] = df[col].apply(
        lambda x: "TCAP Cloud" if "azure" in str(x).lower() else "LDCM"
    )

    # =========================
    # 🔹 Error Name
    # =========================
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

    df["Error Name"] = df[col].apply(find_error)

    # =========================
    # 🔹 Service name
    # =========================
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

    df["Service name"] = df[col].apply(find_service)

    # =========================
    # 🔹 Empty Columns
    # =========================
    df["Change"] = ""
    df["Service Cat."] = ""

    # 👇 เรียง column
    result = df[[
        "System",
        "Change",
        "Error Name",
        "Service name",
        "Service Cat."
    ]]

    return result


if raw_file:
    try:
        df = read_file(raw_file)

        st.subheader("📥 Raw Data")
        st.dataframe(df.head())

        result_df = generate_columns(df)

        st.subheader("✅ Result")
        st.dataframe(result_df.head())

        # Download
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Result",
            data=csv,
            file_name="output.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")
