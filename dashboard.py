# dashboard.py — Housypoint Test Dashboard
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Housypoint Test Dashboard", page_icon="📊", layout="wide")

DATA_FILE = "housypoint_submissions.csv"
USE_SHEETS = st.secrets.get("storage", {}).get("use_sheets", False)
SHEET_NAME = st.secrets.get("storage", {}).get("sheet_name", "Housypoint Test")
PASS_MARK  = 30  # keep in sync with questions.py

def load_data() -> pd.DataFrame:
    if USE_SHEETS:
        import gspread
        from google.oauth2.service_account import Credentials
        creds_dict = st.secrets["gcp_service_account"]
        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]
        credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(credentials)
        sh = client.open(SHEET_NAME)
        ws = sh.sheet1
        values = ws.get_all_records()
        return pd.DataFrame(values)
    else:
        return pd.read_csv(DATA_FILE)

st.title("📊 Housypoint Test Dashboard")

try:
    df = load_data()
    if df.empty:
        st.info("No submissions yet.")
    else:
        # Clean types
        if "total" in df.columns:
            df["total"] = pd.to_numeric(df["total"], errors="coerce")
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        # KPIs
        total_candidates = len(df)
        pass_count = int((df["total"] >= PASS_MARK).sum())
        fail_count = total_candidates - pass_count
        top_score = int(df["total"].max())
        low_score = int(df["total"].min())
        mean_score = round(df["total"].mean(), 2)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Submissions", total_candidates)
        c2.metric("Pass", pass_count)
        c3.metric("Fail", fail_count)
        c4.metric("Top Score", top_score)
        c5.metric("Average Score", mean_score)

        st.markdown("---")

        # Charts
        colA, colB = st.columns(2)
        with colA:
            st.subheader("Score Distribution")
            st.bar_chart(df["total"])

        with colB:
            st.subheader("Pass vs Fail")
            pf = pd.DataFrame({"Status": ["Pass","Fail"], "Count": [pass_count, fail_count]})
            pf = pf.set_index("Status")
            st.bar_chart(pf)

        # Underperformers & toppers
        st.subheader("Lists")
        under = df[df["total"] < PASS_MARK][["timestamp","name","employee_id","total","result"]].sort_values("total")
        top5  = df.sort_values("total", ascending=False).head(5)[["timestamp","name","employee_id","total"]]
        c3, c4 = st.columns(2)
        with c3:
            st.caption("Underperformers (Below Pass)")
            st.dataframe(under, use_container_width=True)
        with c4:
            st.caption("Top 5 Scores")
            st.dataframe(top5, use_container_width=True)

        # Per-MCQ correctness (if stored)
        st.subheader("Per-Question Correctness (MCQs)")
        mcq_cols = [c for c in df.columns if c.endswith("_correct")]
        if mcq_cols:
            pq = pd.DataFrame({
                "Question": [c.replace("_correct","").upper() for c in mcq_cols],
                "Correct %": [round(100*df[c].mean(), 1) for c in mcq_cols]
            })
            st.dataframe(pq, use_container_width=True)
            st.bar_chart(pq.set_index("Question"))
        else:
            st.info("Per-question flags not found in data.")

        # Raw table & export
        st.subheader("All Submissions (raw)")
        st.dataframe(df, use_container_width=True, height=420)
        st.download_button("⬇️ Download CSV", df.to_csv(index=False), "all_housypoint_submissions.csv", "text/csv")

except FileNotFoundError:
    st.info("No local CSV found yet. Once the first submission happens, this dashboard will populate.")
