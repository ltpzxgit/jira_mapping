import pandas as pd

# ===== LOAD =====
jira_file = "JIRA (2).csv"
template_file = "JIRA_LDSO as of 20260228 service mapping_Draft.xlsx"

df_jira = pd.read_csv(jira_file)

# ===== DEFINE TEMPLATE COLUMN =====
# 👇 ใส่ column ตาม LDSO จริง (แก้ได้)
template_columns = [
    'Issue Key',
    'Summary',
    'System',
    'Issue Type',
    'Status',
    'Priority',
    'Assignee',
    'Created',
    'Updated'
]

# ===== CREATE EMPTY DF =====
df_output = pd.DataFrame(columns=template_columns)

# ===== MAP BASIC FIELD =====
df_output['Issue Key'] = df_jira['Issue key']
df_output['Summary'] = df_jira['Summary']
df_output['Issue Type'] = df_jira['Issue Type']
df_output['Status'] = df_jira['Status']
df_output['Priority'] = df_jira['Priority']
df_output['Assignee'] = df_jira['Assignee']
df_output['Created'] = pd.to_datetime(df_jira['Created'], errors='coerce')
df_output['Updated'] = pd.to_datetime(df_jira['Updated'], errors='coerce')

# ===== DERIVE SYSTEM FROM SUMMARY =====
def map_system(summary):
    if pd.isna(summary):
        return None
    
    summary = summary.upper()

    if 'AZURE' in summary:
        return 'TCAP Cloud'
    elif 'L-DCM' in summary:
        return 'LDCM'
    else:
        return 'Other'

df_output['System'] = df_jira['Summary'].apply(map_system)

# ===== EXPORT =====
output_file = "JIRA_LDSO_Output.xlsx"

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df_output.to_excel(writer, sheet_name='JIRA_LDSO', index=False)

print("✅ Done แบบมี System + format ครบ")
