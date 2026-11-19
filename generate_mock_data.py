import os
import json
import numpy as np
import pandas as pd

np.random.seed(42)
os.makedirs("data", exist_ok=True)

FACILITIES = [
    f"{name} {kind}"
    for name, kind in [
        ("Amani", "Health Centre"), ("Baraka", "Medical Clinic"), ("Uzima", "Dispensary"),
        ("Tumaini", "Health Centre"), ("Neema", "Medical Clinic"), ("Upendo", "Hospital"),
        ("Fahari", "Health Centre"), ("Imani", "Medical Clinic"), ("Jambo", "Dispensary"),
        ("Karibu", "Health Centre"), ("Lulu", "Medical Clinic"), ("Mwangaza", "Hospital"),
        ("Nuru", "Health Centre"), ("Pendo", "Medical Clinic"), ("Rehema", "Dispensary"),
        ("Salama", "Health Centre"), ("Taji", "Medical Clinic"), ("Umoja", "Hospital"),
        ("Wema", "Health Centre"), ("Zuri", "Medical Clinic"), ("Asante", "Dispensary"),
        ("Bahati", "Health Centre"), ("Chema", "Medical Clinic"), ("Daima", "Hospital"),
        ("Elimu", "Health Centre"), ("Furaha", "Medical Clinic"), ("Gharama", "Dispensary"),
        ("Hekima", "Health Centre"), ("Inuka", "Medical Clinic"), ("Juhudi", "Hospital"),
        ("Kazi", "Health Centre"), ("Lenana", "Medical Clinic"), ("Maisha", "Dispensary"),
        ("Nyota", "Health Centre"), ("Okoa", "Medical Clinic"), ("Pamoja", "Hospital"),
        ("Raha", "Health Centre"), ("Sifa", "Medical Clinic"),
    ]
]
COUNTIES = ["Nairobi North", "Kiambu West", "Nakuru Central", "Kisumu East", "Mombasa South"]
FAC_COUNTY = {f: COUNTIES[i % len(COUNTIES)] for i, f in enumerate(FACILITIES)}

MONTHS = [
    ("2025", 1, "January"), ("2025", 2, "February"), ("2025", 3, "March"),
    ("2025", 4, "April"), ("2025", 5, "May"), ("2025", 6, "June"),
    ("2025", 7, "July"), ("2025", 8, "August"), ("2025", 9, "September"),
    ("2025", 10, "October"), ("2025", 11, "November"), ("2025", 12, "December"),
    ("2026", 1, "January"), ("2026", 2, "February"), ("2026", 3, "March"),
    ("2026", 4, "April"), ("2026", 5, "May"), ("2026", 6, "June"),
    ("2026", 7, "July"), ("2026", 8, "August"), ("2026", 9, "September"),
    ("2026", 10, "October"),
]

# 1. KHIS PV Snapshot
pv_rows = []
for fac in FACILITIES:
    base_pv = np.random.randint(350, 1400)
    for yr, m_num, m_name in MONTHS:
        q = f"Q{(m_num - 1)//3 + 1}"
        growth = 1.12 if yr == "2026" else 1.0
        pv_val = int(base_pv * growth * np.random.uniform(0.85, 1.20))
        pv_rows.append({
            "organisationunitname": fac,
            "Period": f"{m_name} {yr}",
            "PV": pv_val,
            "Quarter": f"{q} {yr}",
        })
pd.DataFrame(pv_rows).to_csv("data/khis_pv_snapshot.csv.gz", index=False, compression="gzip")

# 2. KHIS ANC Snapshot
anc_rows = []
for fac in FACILITIES:
    for yr, m_num, m_name in MONTHS:
        anc1 = np.random.randint(25, 110)
        anc4 = int(anc1 * np.random.uniform(0.55, 0.85))
        anc_rows.append({
            "facility_name": fac,
            "Year": yr,
            "MonthNum": m_num,
            "Month": m_name,
            "period_id": f"{yr}{m_num:02d}",
            "period_name": f"{m_name} {yr}",
            "ANC_1st_New": anc1,
            "ANC_1st_Under_12w": int(anc1 * np.random.uniform(0.25, 0.45)),
            "ANC_4th_Completed": anc4,
            "ANC_8th_Completed": int(anc4 * np.random.uniform(0.15, 0.35)),
            "ANC_Adol_10_14": np.random.randint(0, 4),
            "ANC_Adol_15_19": np.random.randint(3, 18),
            "ANC_Folic_Only": np.random.randint(5, 25),
            "ANC_IFAS_Combined": int(anc1 * 0.85),
            "ANC_IPTp1": int(anc1 * 0.70),
            "ANC_IPTp2": int(anc1 * 0.55),
            "ANC_IPTp3": int(anc1 * 0.40),
            "ANC_Iron_Only": np.random.randint(5, 20),
            "ANC_LLIN": int(anc1 * 0.75),
            "ANC_Revisits": int(anc1 * np.random.uniform(1.4, 2.3)),
            "ANC_Syphilis_Pos": np.random.randint(0, 3),
            "ANC_Syphilis_Tested": int(anc1 * 0.90),
            "ANC_Youth_20_24": int(anc1 * 0.35),
        })
pd.DataFrame(anc_rows).to_csv("data/khis_anc_snapshot.csv.gz", index=False, compression="gzip")

# 3. KHIS OPD Snapshot
opd_rows = []
for fac in FACILITIES:
    for yr, m_num, m_name in MONTHS:
        o5_f = np.random.randint(180, 650)
        o5_m = np.random.randint(140, 520)
        u5_f = np.random.randint(90, 320)
        u5_m = np.random.randint(90, 320)
        opd_rows.append({
            "facility_name": fac,
            "Year": yr,
            "MonthNum": m_num,
            "Month": m_name,
            "period_id": f"{yr}{m_num:02d}",
            "period_name": f"{m_name} {yr}",
            "OPD_O5_Female": o5_f,
            "OPD_O5_Male": o5_m,
            "OPD_U5_Female": u5_f,
            "OPD_U5_Male": u5_m,
            "OPD_Under5_Total": u5_f + u5_m,
            "OPD_Over5_Total": o5_f + o5_m,
            "OPD_Total_Workload": o5_f + o5_m + u5_f + u5_m,
        })
pd.DataFrame(opd_rows).to_csv("data/khis_opd_snapshot.csv.gz", index=False, compression="gzip")

# 4. KHIS KPI Snapshot
kpi_indicators = [
    ("MOH 711 Normal Deliveries", (15, 65)),
    ("MOH 711 Live birth", (15, 68)),
    ("MOH 711 Caesarian Sections", (1, 12)),
    ("MOH 711 Assisted vaginal delivery", (0, 4)),
    ("MOH 711 Breach Delivery", (0, 3)),
    ("MOH 711 Births with low APGAR score", (0, 4)),
    ("MOH 711 Fresh Still Birth", (0, 2)),
    ("MOH 711 Macerated still Birth", (0, 2)),
    ("MOH 711 Neonatal deaths 0-28 Days", (0, 2)),
    ("MOH 711 PPH (Post Partum Haemorrage) A", (0, 3)),
    ("MOH 711 Rev 2020_Neonatal deaths due to Asphyxia", (0, 2)),
    ("MOH 711 Rev 2020_Perinatal Deaths 0-7 days", (0, 2)),
]
kpi_cols = {"organisationunitname": FACILITIES}
for ind, (low, high) in kpi_indicators:
    for yr, _, m_name in MONTHS:
        kpi_cols[f"{ind} {m_name} {yr}"] = np.random.randint(low, high + 1, size=len(FACILITIES))
pd.DataFrame(kpi_cols).to_csv("data/khis_kpi_snapshot.csv.gz", index=False, compression="gzip")

# 5. MoniTrac Finance Snapshot
fin_cols = {"organisationunitname": FACILITIES}
months_2026 = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November"]
for m in months_2026:
    rev = np.random.randint(250000, 1200000, size=len(FACILITIES))
    exp = (rev * np.random.uniform(0.68, 0.98, size=len(FACILITIES))).astype(int)
    fin_cols[f"kny - fr - Total revenu {m} 2026"] = rev
    fin_cols[f"kny - fr - Total expenses {m} 2026"] = exp
pd.DataFrame(fin_cols).to_csv("data/monitrac_finance_snapshot.csv.gz", index=False, compression="gzip")

# 6. MoniTrac PSS Snapshot
pss_rows = []
for idx, fac in enumerate(FACILITIES[:25]):
    for yr, m_num, m_name in MONTHS[-12:]:
        score = round(np.random.uniform(74.0, 96.0), 1)
        pss_rows.append({
            "organisationunitid": f"ORG_{idx+1:03d}",
            "organisationunitname": fac,
            "periodid": f"{yr}{m_num:02d}",
            "periodname": f"{m_name} {yr}",
            "Net_Satisfaction_Score": score,
            "Survey_Score": score,
            "Obtained_Points": int(score * 2),
            "Max_Points": 200,
            "Year": int(yr),
            "Month_Num": m_num,
            "Quarter": f"Q{(m_num - 1)//3 + 1} {yr}",
        })
pd.DataFrame(pss_rows).to_csv("data/monitrac_pss_snapshot.csv.gz", index=False, compression="gzip")

# 7. MoniTrac Mentees Snapshot
mentee_rows = []
cadres = ["Nurse", "Clinical Officer", "Midwife", "Lab Technologist", "Facility Manager"]
tracks = ["Medical Quality", "Management & Finance"]
curricula = ["Maternal & Newborn Care", "Infection Prevention", "Financial Management", "Pharmacy & Inventory"]
mentors = ["Mentor A", "Mentor B", "Mentor C", "Mentor D"]

for ev_idx in range(1, 540):
    fac = FACILITIES[ev_idx % len(FACILITIES)]
    ben_id = (ev_idx % 250) + 1
    yr, m_num, m_name = MONTHS[ev_idx % len(MONTHS)]
    track = tracks[ev_idx % 2]
    curr = curricula[ev_idx % len(curricula)]
    mentee_rows.append({
        "event_uid": f"EV_{ev_idx:05d}",
        "tei": f"TEI_{ben_id:04d}",
        "enrollment_uid": f"ENR_{ben_id:04d}",
        "event_date_raw": f"{yr}-{m_num:02d}-15",
        "facility_name": fac,
        "ou_hierarchy": f"National / {FAC_COUNTY[fac]} / {fac}",
        "event_status": "COMPLETED",
        "modality_code": "IN_PERSON" if ev_idx % 3 != 0 else "VIRTUAL",
        "activity_modality_raw": "On-site Coaching" if ev_idx % 3 != 0 else "Virtual Mentoring",
        "virtual_platform_raw": "" if ev_idx % 3 != 0 else "Zoom",
        "minutes_raw": 90,
        "special_training": "No",
        "first_name": f"Staff{ben_id}",
        "last_name": f"Member{ben_id}",
        "trainer_raw": mentors[ev_idx % len(mentors)],
        "lessons": f"Lesson {(ev_idx % 6) + 1}",
        "modules": curr,
        "gender_raw": "Female" if ben_id % 3 != 0 else "Male",
        "cadre_raw": cadres[ben_id % len(cadres)],
        "is_sister": "No",
        "program_phase": "Active Phase",
        "id_number": f"ID{10000 + ben_id}",
        "event_date": f"{yr}-{m_num:02d}-15",
        "Year": int(yr),
        "Month_Num": m_num,
        "Month_Label": m_name[:3],
        "Year_Month": f"{yr}-{m_num:02d}",
        "Quarter_Label": f"Q{(m_num - 1)//3 + 1} {yr}",
        "mentee_name": f"Staff{ben_id} Member{ben_id}",
        "beneficiary_uid": f"BEN-{ben_id:04d}",
        "county": FAC_COUNTY[fac],
        "Modality": "In-Person" if ev_idx % 3 != 0 else "Virtual",
        "Delivery_Mode": "On-Site" if ev_idx % 3 != 0 else "Remote",
        "Virtual_Platform": "N/A" if ev_idx % 3 != 0 else "Zoom",
        "Minutes": 90,
        "Gender": "Female" if ben_id % 3 != 0 else "Male",
        "Cadre": cadres[ben_id % len(cadres)],
        "Mentors": mentors[ev_idx % len(mentors)],
        "Mentor_Track": track,
        "Mentor_Cohort": f"Cohort {(ev_idx % 3) + 1}",
        "Curriculum": curr,
        "Modules_Pretty": curr,
        "Session_UID": f"SES_{ev_idx // 2:04d}",
        "Mentor_Session_UID": f"MSES_{ev_idx // 2:04d}",
    })
pd.DataFrame(mentee_rows).to_csv("data/monitrac_mentees_snapshot.csv.gz", index=False, compression="gzip")

# 8. QSC Analytics Workbook (Cohort 1 & 2)
qsc_mgmt = pd.DataFrame({
    "Name of the Health Facility": FACILITIES[:24],
    "Cohort ": ["Cohort 1" if i < 12 else "Cohort 2" for i in range(24)],
    "Cohort": ["Cohort 1" if i < 12 else "Cohort 2" for i in range(24)],
    "man - qsc - Module 1 - Percentage Baseline": np.round(np.random.uniform(45, 68, 24), 1),
    "man - qsc - Module 1 - Percentage Endline": np.round(np.random.uniform(76, 94, 24), 1),
    "man - qsc - Module 2 - Percentage Baseline": np.round(np.random.uniform(42, 65, 24), 1),
    "man - qsc - Module 2 - Percentage Endline": np.round(np.random.uniform(74, 92, 24), 1),
    "man - qsc - Module 3 - Percentage Baseline": np.round(np.random.uniform(48, 70, 24), 1),
    "man - qsc - Module 3 - Percentage Endline": np.round(np.random.uniform(78, 95, 24), 1),
    "man - qsc - Module 4 - Percentage baseline": np.round(np.random.uniform(44, 66, 24), 1),
    "man - qsc - Module 4 - Percentage Endline": np.round(np.random.uniform(75, 93, 24), 1),
})
qsc_med = pd.DataFrame({
    "Name of the Health Facility": FACILITIES[:24],
    "Cohort ": ["Cohort 1" if i < 12 else "Cohort 2" for i in range(24)],
    "Cohort": ["Cohort 1" if i < 12 else "Cohort 2" for i in range(24)],
    "med - qsc - Module 1 - Back to basics - Percentage Baseline": np.round(np.random.uniform(50, 70, 24), 1),
    "med - qsc - Module 1 - Back to basics - Percentage Endline": np.round(np.random.uniform(80, 96, 24), 1),
    "med - qsc - Module 2 - Safe baby - Percentage Baseline": np.round(np.random.uniform(46, 68, 24), 1),
    "med - qsc - Module 2 - Safe baby - Percentage Endline": np.round(np.random.uniform(78, 95, 24), 1),
    "med - qsc - Module 3 - Safe mother - Percentage Baseline": np.round(np.random.uniform(48, 69, 24), 1),
    "med - qsc - Module 3 - Safe mother - Percentage Endline": np.round(np.random.uniform(79, 94, 24), 1),
    "med - qsc - Module 4 - healthy children - Percentage Baseline": np.round(np.random.uniform(45, 67, 24), 1),
    "med - qsc - Module 4 - healthy children - Percentage Endline": np.round(np.random.uniform(77, 93, 24), 1),
    "med - qsc - Module 5 - top burdens of disease - Percentage baseline": np.round(np.random.uniform(44, 65, 24), 1),
    "med - qsc - Module 5 - top burdens of disease - Percentage Endline": np.round(np.random.uniform(76, 92, 24), 1),
})
qsc_med["med - qsc - Total final percentage"] = qsc_med[[
    "med - qsc - Module 1 - Back to basics - Percentage Endline",
    "med - qsc - Module 2 - Safe baby - Percentage Endline",
    "med - qsc - Module 3 - Safe mother - Percentage Endline",
    "med - qsc - Module 4 - healthy children - Percentage Endline",
    "med - qsc - Module 5 - top burdens of disease - Percentage Endline",
]].mean(axis=1).round(1)

with pd.ExcelWriter("data/Cohort 1&2 QSC Analytics final.xlsx", engine="openpyxl") as writer:
    qsc_mgmt.to_excel(writer, sheet_name="Management QSC Performance", index=False)
    qsc_med.to_excel(writer, sheet_name="Medical QSC Performance", index=False)

# 9. Cohort 3 QSC Workbook
c3_med = pd.DataFrame({
    "organisationunitname": FACILITIES[24:],
    " Baseline Module 1 - Back to basics - Percentage": np.round(np.random.uniform(48, 68, 14), 1),
    "Endline - Module 1 - Back to basics - Percentage": np.round(np.random.uniform(78, 94, 14), 1),
})
c3_mgmt = pd.DataFrame({
    "print": FACILITIES[24:],
    "Baseline Score Management Module 1 Percentage": np.round(np.random.uniform(45, 66, 14), 1),
    "Endline Score Management Module 1 Percentage": np.round(np.random.uniform(75, 92, 14), 1),
})
with pd.ExcelWriter("data/Cleaned_Cohort_3_QSC.xlsx", engine="openpyxl") as writer:
    c3_med.to_excel(writer, sheet_name="Medical QSC Performance", index=False)
    c3_mgmt.to_excel(writer, sheet_name="Management QSC Performance", index=False)

# 10. Comments JSON
with open("data/data_quality_comments.json", "w") as f:
    json.dump([], f)

print("All synthetic datasets generated successfully in data/!")
