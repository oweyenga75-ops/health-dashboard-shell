import os
import pandas as pd

def _norm_fac_key(name: str) -> str:
    return str(name).strip().lower()

def sync_monitrac_mentees(force_live: bool = False) -> pd.DataFrame:
    path = os.path.join("data", "monitrac_mentees_snapshot.csv.gz")
    return pd.read_csv(path, compression="gzip") if os.path.exists(path) else pd.DataFrame()

def build_facility_coverage_matrix(df_mentees: pd.DataFrame) -> pd.DataFrame:
    pv_path = os.path.join("data", "khis_pv_snapshot.csv.gz")
    if os.path.exists(pv_path):
        facilities = sorted(pd.read_csv(pv_path, compression="gzip")["organisationunitname"].unique())
    elif not df_mentees.empty and "facility_name" in df_mentees.columns:
        facilities = sorted(df_mentees["facility_name"].dropna().unique())
    else:
        return pd.DataFrame()

    rows = []
    for fac in facilities:
        sub = df_mentees[df_mentees["facility_name"] == fac] if not df_mentees.empty else pd.DataFrame()
        if sub.empty:
            rows.append({
                "Facility": fac,
                "Coverage_Status": "🔴 Zero Reach Gap",
                "Unique_Mentees": 0,
                "Medical_Mentees": 0,
                "Management_Mentees": 0,
                "Onsite_Sessions": 0,
                "Virtual_Sessions": 0,
                "Last_Mentorship": "None",
                "Total_Sessions": 0,
                "Total_Events": 0,
            })
            continue

        uniq = int(sub["beneficiary_uid"].nunique())
        med_u = int(sub[sub["Curriculum"].str.contains("Medical", case=False, na=False)]["beneficiary_uid"].nunique())
        mgt_u = int(sub[sub["Curriculum"].str.contains("Management", case=False, na=False)]["beneficiary_uid"].nunique())
        onsite_s = int(sub[sub["Delivery_Mode"].str.contains("Onsite|In-Person", case=False, na=False)]["Session_UID"].nunique())
        virt_s = int(sub[sub["Delivery_Mode"].str.contains("Virtual", case=False, na=False)]["Session_UID"].nunique())
        last_dt = str(sub["event_date"].max()) if "event_date" in sub.columns else "2026-10-15"

        if med_u > 0 and mgt_u > 0:
            status = "🟢 Full Dual Coverage"
        elif med_u > 0:
            status = "🟡 Medical Only"
        elif mgt_u > 0:
            status = "🟡 Management Only"
        else:
            status = "🔴 Zero Reach Gap"

        rows.append({
            "Facility": fac,
            "Coverage_Status": status,
            "Unique_Mentees": uniq,
            "Medical_Mentees": med_u,
            "Management_Mentees": mgt_u,
            "Onsite_Sessions": onsite_s,
            "Virtual_Sessions": virt_s,
            "Last_Mentorship": last_dt,
            "Total_Sessions": int(sub["Session_UID"].nunique()),
            "Total_Events": int(len(sub)),
        })
    return pd.DataFrame(rows)
