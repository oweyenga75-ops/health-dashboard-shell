import os
import pandas as pd

def get_live_pv_and_kpi_frames(pv_uid="", kpi_uid="", target_period=None, force_live=False):
    pv_path = os.path.join("data", "khis_pv_snapshot.csv.gz")
    kpi_path = os.path.join("data", "khis_kpi_snapshot.csv.gz")
    df_pv = pd.read_csv(pv_path, compression="gzip") if os.path.exists(pv_path) else pd.DataFrame()
    df_kpi = pd.read_csv(kpi_path, compression="gzip") if os.path.exists(kpi_path) else pd.DataFrame()
    return df_pv, df_kpi

def get_live_cleaned_dataset(pv_uid="", kpi_uid="", target_period=None):
    return get_live_pv_and_kpi_frames(pv_uid, kpi_uid, target_period)

def get_live_anc_frame(ref_viz_uid="", force_live=False):
    anc_path = os.path.join("data", "khis_anc_snapshot.csv.gz")
    return pd.read_csv(anc_path, compression="gzip", dtype={"Year": str}) if os.path.exists(anc_path) else pd.DataFrame()

def get_live_opd_frame(ref_viz_uid="", force_live=False):
    opd_path = os.path.join("data", "khis_opd_snapshot.csv.gz")
    return pd.read_csv(opd_path, compression="gzip", dtype={"Year": str}) if os.path.exists(opd_path) else pd.DataFrame()
