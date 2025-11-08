# app.py — Housypoint Test (uses questions.py)
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

from questions import (
    MCQ_QUESTIONS, LONG_QUESTIONS,
    MCQ_MARKS, LONG_MARKS, PASS_MARK, TEST_DURATION_MIN
)

# ---- BASIC CONFIG ----
st.set_page_config(page_title="Housypoint Inspection Test", page_icon="🧰", layout="centered")
ADMIN_KEY = "housypoint-admin-123"   # change
DATA_FILE = "housypoint_submissions.csv"

# ---- OPTIONAL GOOGLE SHEETS BACKEND ----
USE_SHEETS = st.secrets.get("storage", {}).get("use_sheets", False)
SHEET_NAME = st.secrets.get("storage", {}).get("sheet_name", "Housypoint Test")

def save_row(row: dict):
    """Save to Google Sheets if configured, else CSV."""
    if USE_SHEETS:
        import gspread
        from google.oauth2.service_account import Credentials
        creds_dict = st.secrets["gcp_service_account"]
        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]
        credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(credentials)

        # Open by name (first match); create if missing
        try:
            sh = client.open(SHEET_NAME)
        except gspread.SpreadsheetNotFound:
            sh = client.create(SHEET_NAME)
        ws = sh.sheet1
        if ws.row_count == 1 and ws.col_count == 1 and ws.get_all_values() == [['']]:
            ws.clear()
        # header
        headers = list(row.keys())
        if not ws.get_all_values():
            ws.append_row(headers)
        # ensure same order
        ws.append_row([row.get(h, "") for h in headers])
    else:
        try:
            df_old = pd.read_csv(DATA_FILE)
            df_new = pd.concat([df_old, pd.DataFrame([row])], ignore_index=True)
        except Exception:
            df_new = pd.DataFrame([row])
        df_new.to_csv(DATA_FILE, index=False)

# ---- STYLE ----
st.markdown("""
<style>
div.stButton > button:first-child { border-radius:10px; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ---- TIMER ----
if "deadline" not in st.session_state:
    st.session_state.deadline = datetime.utcnow() + timedelta(minutes=TEST_DURATION_MIN)
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "locked" not in st.session_state:
    st.session_state.locked = False

def time_left():
    remaining = st.session_state.deadline - datetime.utcnow()
    secs = int(remaining.total_seconds())
    if secs <= 0:
        return "00:00", 0
    return f"{secs//60:02d}:{secs%60:02d}", secs

tstr, tsec = time_left()
if tsec <= 0 and not st.session_state.locked:
    st.session_state.locked = True

st.title("🏗️ Housypoint Employee Inspection Knowledge Test")
st.info(f"⏱ Time left: **{tstr}**  •  Test locks automatically at 00:00")

# ---- Candidate Info ----
name  = st.text_input("Full Name", disabled=st.session_state.locked or st.session_state.submitted)
empid = st.text_input("Employee ID", disabled=st.session_state.locked or st.session_state.submitted)
email = st.text_input("Email (optional)", disabled=st.session_state.locked or st.session_state.submitted)

disabled = st.session_state.locked or st.session_state.submitted
st.divider()

# ---- Render Questions ----
st.subheader("Section A – MCQs (auto-scored)")
for q in MCQ_QUESTIONS:
    st.radio(q["question"], q["options"], index=None, key=q["id"], disabled=disabled)

st.subheader("Section B – Long Answers (auto-checked by rubric)")
for q in LONG_QUESTIONS:
    st.text_area(q["prompt"], key=q["id"], height=140, disabled=disabled)

# ---- Scoring helpers ----
def mcq_score_and_flags():
    score = 0
    flags = {}
    for q in MCQ_QUESTIONS:
        sel = st.session_state.get(q["id"])
        correct = (sel == q["answer"])
        flags[q["id"]] = {"selected": sel, "correct": correct}
        if correct: score += MCQ_MARKS
    return score, flags

def rubric_score(text: str, keywords: list):
    if not text:
        return 0, []
    t = text.lower()
    hits = [kw for kw in keywords if kw.lower() in t]
    # 0..LONG_MARKS based on coverage
    frac = min(1.0, len(hits) / max(3, len(keywords)//2))
    return int(round(frac * LONG_MARKS)), hits

def long_scores():
    total = 0
    detail = {}
    for q in LONG_QUESTIONS:
        s, hits = rubric_score(st.session_state.get(q["id"], ""), q["keywords"])
        total += s
        detail[q["id"]] = {"score": s, "hits": hits}
    return total, detail

# ---- Submit ----
col1, col2 = st.columns(2)
with col1:
    submit = st.button("✅ Submit", disabled=disabled or not name or not empid)
with col2:
    reset  = st.button("🔁 Reset (clear answers)", disabled=st.session_state.submitted)

if reset:
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

if st.session_state.locked and not st.session_state.submitted:
    st.error("Time is up. The test is locked.")
elif submit:
    mcq_total, mcq_flags = mcq_score_and_flags()
    long_total, long_detail = long_scores()

    total_marks = mcq_total + long_total
    result = "PASS ✅" if total_marks >= PASS_MARK else "FAIL ❌"

    row = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name, "employee_id": empid, "email": email,
        "mcq_score": mcq_total, "long_score": long_total,
        "total": total_marks, "result": result,
    }
    # store selections per MCQ
    for q in MCQ_QUESTIONS:
        row[f"{q['id']}_selected"] = mcq_flags[q["id"]]["selected"]
        row[f"{q['id']}_correct"]  = mcq_flags[q["id"]]["correct"]
    # store long answers + keyword hits
    for q in LONG_QUESTIONS:
        ans = st.session_state.get(q["id"], "")
        row[f"{q['id']}_answer"] = ans
        row[f"{q['id']}_hits"]   = ", ".join(long_detail[q["id"]]["hits"])
        row[f"{q['id']}_score"]  = long_detail[q["id"]]["score"]

    save_row(row)
    st.session_state.submitted = True

    st.success(f"Submitted! Total: **{total_marks}**  •  MCQs: {mcq_total}  •  Long: {long_total}  •  {result}")
    st.download_button(
        "⬇️ Download your submission (CSV row)",
        data=pd.DataFrame([row]).to_csv(index=False),
        file_name=f"{empid}_{name.replace(' ','_')}_submission.csv",
        mime="text/csv"
    )

# ---- Admin mini-view ----
st.divider()
st.subheader("🔐 Admin Panel")
key = st.text_input("Enter Admin Key", type="password")
if key == ADMIN_KEY:
    st.success("Access granted.")
    try:
        if USE_SHEETS:
            st.info("Storage: Google Sheets")
            st.write("Open the Sheets file to view all rows.")
        else:
            df = pd.read_csv(DATA_FILE)
            st.dataframe(df, use_container_width=True, height=420)
            st.download_button("⬇️ Download all (CSV)", df.to_csv(index=False), "all_submissions.csv", "text/csv")
    except Exception as e:
        st.warning(f"No submissions yet or read error: {e}")
elif key:
    st.error("Invalid admin key.")
