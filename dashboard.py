# dashboard_secure.py — Analytics for Housypoint Secure Assessment
import streamlit as st
import pandas as pd
from datetime import datetime
from questions import ANSWER_KEY, MCQ_SECTIONS, PASS_MARK

st.set_page_config(page_title="Housypoint Test Dashboard", page_icon="📊", layout="wide")
DATA_FILE = "secure_submissions.csv"

st.title("📊 Housypoint Test Dashboard (Secure)")

# ----------------- DATA LOADING -----------------
@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # basic cleanup
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    numeric_cols = ["mcq_score","long_score","total","warnings"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

try:
    df = load_data(DATA_FILE)
except FileNotFoundError:
    st.info("No submissions CSV found yet. Once the first candidate submits, this dashboard will populate.")
    st.stop()

if df.empty:
    st.info("No rows yet. Wait for the first submission.")
    st.stop()

# ----------------- FILTERS -----------------
with st.sidebar:
    st.header("Filters")
    date_min, date_max = df["timestamp"].min(), df["timestamp"].max()
    _dr = st.date_input("Date range", value=(date_min.date(), date_max.date()))
    if isinstance(_dr, tuple) and len(_dr) == 2:
        d1, d2 = _dr
        df = df[(df["timestamp"].dt.date >= d1) & (df["timestamp"].dt.date <= d2)]
    name_q = st.text_input("Search by name / ID / mobile / email").strip().lower()
    if name_q:
        df = df[
            df["name"].str.lower().str.contains(name_q, na=False)
            | df["employee_id"].astype(str).str.lower().str.contains(name_q, na=False)
            | df["mobile"].astype(str).str.lower().str.contains(name_q, na=False)
            | df["email"].str.lower().str.contains(name_q, na=False)
        ]
    warn_limit = st.slider("Show entries with warnings ≥", 0, int(df["warnings"].max() or 0), 0)
    df = df[df["warnings"] >= warn_limit]

# ----------------- KPIs -----------------
total_candidates = len(df)
pass_count = int((df["total"] >= PASS_MARK).sum())
fail_count = total_candidates - pass_count
top_score = int(df["total"].max())
low_score = int(df["total"].min())
avg_score = round(df["total"].mean(), 2)
avg_warn = round(df["warnings"].mean(), 2)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Submissions", total_candidates)
c2.metric("Pass", pass_count)
c3.metric("Fail", fail_count)
c4.metric("Top Score", top_score)
c5.metric("Avg Score", avg_score)
c6.metric("Avg Warnings", avg_warn)

st.markdown("---")

# ----------------- CHARTS -----------------
colA, colB = st.columns(2)
with colA:
    st.subheader("Score Distribution")
    st.bar_chart(df["total"])
with colB:
    st.subheader("Pass vs Fail")
    pf = pd.DataFrame({"Status": ["Pass","Fail"], "Count": [pass_count, fail_count]}).set_index("Status")
    st.bar_chart(pf)

# ----------------- LISTS -----------------
st.subheader("Top & Underperformers")
left, right = st.columns(2)

with left:
    st.caption("Top 10")
    st.dataframe(
        df.sort_values(["total","timestamp"], ascending=[False, True])
          .head(10)[["timestamp","name","employee_id","mobile","email","total","warnings"]],
        use_container_width=True
    )

with right:
    st.caption("Underperformers (Below Pass)")
    st.dataframe(
        df[df["total"] < PASS_MARK]
          .sort_values(["total","timestamp"])
          [["timestamp","name","employee_id","mobile","email","total","warnings"]],
        use_container_width=True
    )

# ----------------- PER-QUESTION ACCURACY (MCQs) -----------------
st.subheader("Per-Question Accuracy (MCQs)")
# find the MCQ answer columns (they end with _ans in secure_submissions.csv)
mcq_ids = [q["id"] for q in MCQ_SECTIONS]
present_cols = [f"{qid}_ans" for qid in mcq_ids if f"{qid}_ans" in df.columns]

if present_cols:
    records = []
    for qid in mcq_ids:
        col = f"{qid}_ans"
        if col not in df.columns: 
            continue
        total = df[col].notna().sum()
        correct = (df[col] == ANSWER_KEY.get(qid)).sum()
        acc = round(100 * correct / total, 1) if total else 0.0
        records.append({"Question": qid, "Answered": int(total), "Correct": int(correct), "Accuracy %": acc})
    acc_df = pd.DataFrame(records)
    st.dataframe(acc_df, use_container_width=True)
    st.bar_chart(acc_df.set_index("Question")["Accuracy %"])
else:
    st.info("Per-question answer columns not found in CSV (will appear after first few submissions).")

# ----------------- RAW DATA & EXPORT -----------------
st.subheader("All Submissions (Raw)")
st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True, height=430)
st.download_button("⬇️ Download CSV", df.to_csv(index=False), "secure_submissions_filtered.csv", "text/csv")

# ----------------- QUICK AUDIT QUERIES -----------------
st.markdown("### Quick Audit")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("**Multiple Warnings (≥2)**")
    mul = df[df["warnings"] >= 2][["timestamp","name","employee_id","mobile","email","warnings","total"]]
    st.dataframe(mul, use_container_width=True)
with col2:
    st.write("**High Scorers with Warnings**")
    hs = df[(df["total"] >= PASS_MARK) & (df["warnings"] >= 1)][["timestamp","name","employee_id","total","warnings"]]
    st.dataframe(hs, use_container_width=True)
with col3:
    st.write("**Failed with 0 Warnings**")
    fw = df[(df["total"] < PASS_MARK) & (df["warnings"] == 0)][["timestamp","name","employee_id","total","warnings"]]
    st.dataframe(fw, use_container_width=True)

