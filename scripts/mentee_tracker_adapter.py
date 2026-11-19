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
        rows.append({
            "Facility": fac,
            "Unique_Mentees": int(sub["beneficiary_uid"].nunique()) if not sub.empty else 0,
            "Total_Sessions": int(sub["Session_UID"].nunique()) if not sub.empty else 0,
            "Total_Events": int(len(sub)),
            "Status": "Active" if len(sub) > 0 else "Pending",
        })
    return pd.DataFrame(rows)
