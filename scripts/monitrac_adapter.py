import os
from datetime import datetime
import pandas as pd

def _norm_key(name):
    return str(name).strip().lower()

def _get_active_38_roster():
    pv_path = os.path.join("data", "khis_pv_snapshot.csv.gz")
    if os.path.exists(pv_path):
        facs = sorted(pd.read_csv(pv_path, compression="gzip")["organisationunitname"].unique())
        return {_norm_key(f): f for f in facs}
    return {}

def _rolling_12_pe_codes():
    now = datetime(2026, 10, 1)
    codes = []
    y, m = now.year, now.month
    for _ in range(12):
        codes.append(f"{y}{m:02d}")
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    return sorted(codes)

def sync_monitrac_finance(year=2026, force_live=False):
    path = os.path.join("data", "monitrac_finance_snapshot.csv.gz")
    return pd.read_csv(path, compression="gzip") if os.path.exists(path) else pd.DataFrame()

def sync_monitrac_pss(force_live=False):
    path = os.path.join("data", "monitrac_pss_snapshot.csv.gz")
    return pd.read_csv(path, compression="gzip") if os.path.exists(path) else pd.DataFrame()
