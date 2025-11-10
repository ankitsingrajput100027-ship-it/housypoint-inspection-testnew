# app_secure.py — Secure Housypoint Assessment (50 Qs)
# Anti-cheat: one-question flow, no back, blur previous, window-change detector (warn 1x, then terminate),
# Mandatory mobile + email, 60-min timer, CSV save.

import re
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit.components.v1 import html as st_html
from streamlit_js_eval import get_geolocation, streamlit_js_eval  # used to read JS values (visibility/localStorage)

from questions import (
    MCQ_QUESTIONS, LONG_QUESTIONS,
    MCQ_MARKS, LONG_MARKS, PASS_MARK, TEST_DURATION_MIN
)

st.set_page_config(page_title="Housypoint Secure Test", page_icon="🛡️", layout="centered")

DATA_FILE = "secure_submissions.csv"
ADMIN_KEY = "housypoint-admin-123"  # change if you like

# ---------- Styles ----------
st.markdown("""
<style>
/* card */
.hp-card {border:1px solid #1f2937; border-radius:14px; padding:14px 16px; margin:10px 0; background:#0b1220;}
.hp-blur {filter: blur(4px); pointer-events:none;}
.hp-locked {opacity:0.4;}
/* buttons */
div.stButton > button:first-child { border-radius:10px; font-weight:600; }
.hp-badge {background:#0ea5e9; color:white; padding:2px 8px; border-radius:999px; font-size:12px;}
.hp-warning {background:#331; border:1px solid #a33; color:#fbb; padding:10px 12px; border-radius:8px;}
.hp-info {background:#0b2239; border:1px solid #174a7a; color:#cde; padding:10px 12px; border-radius:8px;}
.hp-timer {font-weight:700; color:#60a5fa;}
</style>
""", unsafe_allow_html=True)

# ---------- Session init ----------
if "started" not in st.session_state: st.session_state.started = False
if "index" not in st.session_state: st.session_state.index = 0  # 0..49
if "answers" not in st.session_state: st.session_state.answers = {}  # id -> selected/typed
if "lock_map" not in st.session_state: st.session_state.lock_map = {}  # id -> True when locked
if "deadline" not in st.session_state: st.session_state.deadline = datetime.utcnow() + timedelta(minutes=TEST_DURATION_MIN)
if "terminated" not in st.session_state: st.session_state.terminated = False
if "warned" not in st.session_state: st.session_state.warned = False

TOTAL_Q = len(MCQ_QUESTIONS) + len(LONG_QUESTIONS)  # 50

# ---------- Inject tiny JS listener to count tab changes (saved in localStorage) ----------
st_html("""
<script>
(function(){
  // initialize counters if missing
  if(!localStorage.getItem('hp_blur_count')) localStorage.setItem('hp_blur_count','0');
  if(!localStorage.getItem('hp_blur_last')) localStorage.setItem('hp_blur_last','');

  function incBlur(reason){
    const c = parseInt(localStorage.getItem('hp_blur_count')||'0') + 1;
    localStorage.setItem('hp_blur_count', String(c));
    localStorage.setItem('hp_blur_last', new Date().toISOString() + ' ' + reason);
  }

  window.addEventListener('blur', ()=>incBlur('window-blur'));
  document.addEventListener('visibilitychange', ()=>{
    if(document.hidden){ incBlur('visibility-hidden'); }
  });
})();
</script>
""", height=0)

# Read blur count each run
blur_count = 0
try:
    blur_count = int(streamlit_js_eval(js_expressions="localStorage.getItem('hp_blur_count') || '0'", key="blur-read", want_output=True) or 0)
except:
    blur_count = 0

# ---------- Timer ----------
def time_left():
    remaining = st.session_state.deadline - datetime.utcnow()
    s = int(remaining.total_seconds())
    if s <= 0: return "00:00", 0
    return f"{s//60:02d}:{s%60:02d}", s

tstr, tsecs = time_left()
if tsecs <= 0 and not st.session_state.terminated:
    st.session_state.terminated = True

# ---------- Header ----------
left, right = st.columns([0.7, 0.3])
with left:
    st.markdown("### 🛡️ Housypoint Secure Inspection Assessment")
    st.caption("One-question-at-a-time • No back • Window change monitored")
with right:
    st.markdown(f"<div class='hp-info'><span class='hp-timer'>⏱ Time: {tstr}</span><br/><span class='hp-badge'>{TOTAL_Q} Questions</span></div>", unsafe_allow_html=True)

# ---------- Candidate details ----------
def valid_mobile(m): return re.fullmatch(r"[6-9]\d{9}", m or "") is not None
def valid_email(e):  return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", e or "") is not None

if not st.session_state.started:
    st.markdown("<div class='hp-info'>Refreshing the page resets progress. Keep this tab active. "
                "Switching tabs triggers anti-cheat (1 warning, 2nd time terminates).</div>", unsafe_allow_html=True)
    name = st.text_input("Full Name *")
    empid = st.text_input("Employee ID *")
    mobile = st.text_input("Mobile Number * (10 digits)", max_chars=10)
    email = st.text_input("Email *")

    agree = st.checkbox("I understand that switching tabs/minimizing will terminate my test after one warning.", value=False)
    start = st.button("🚀 Start Test", type="primary",
                      disabled=not(name and empid and valid_mobile(mobile) and valid_email(email) and agree))

    if start:
        st.session_state.started = True
        st.session_state.cand = {"name": name, "employee_id": empid, "mobile": mobile, "email": email}
        st.experimental_rerun()

# ---------- Termination for cheating or time over ----------
if st.session_state.started and not st.session_state.terminated:
    if blur_count >= 1 and not st.session_state.warned:
        st.session_state.warned = True
        st.warning("⚠️ Window change detected. This is your **only warning**. "
                   "Next time the test will be terminated automatically.")
    elif blur_count >= 2:
        st.session_state.terminated = True

if st.session_state.terminated and st.session_state.started:
    st.error("❌ Cheater detected / Time over. Your test has been terminated.")
    # Save partial
    # build row from whatever is answered
    cand = st.session_state.get("cand", {})
    row = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "name": cand.get("name",""),
        "employee_id": cand.get("employee_id",""),
        "mobile": cand.get("mobile",""),
        "email": cand.get("email",""),
        "status": "TERMINATED",
        "reason": "TIME_OVER" if tsecs<=0 else "WINDOW_CHANGE_2X",
        "answered": len(st.session_state.answers),
    }
    try:
        df_old = pd.read_csv(DATA_FILE)
        df_new = pd.concat([df_old, pd.DataFrame([row])], ignore_index=True)
    except Exception:
        df_new = pd.DataFrame([row])
    df_new.to_csv(DATA_FILE, index=False)
    st.stop()

# ---------- Build unified list of 50 questions ----------
ALL_QUESTIONS = MCQ_QUESTIONS + LONG_QUESTIONS  # last 5 are descriptive
is_mcq = lambda idx: idx < len(MCQ_QUESTIONS)

def render_question(idx: int):
    q = ALL_QUESTIONS[idx]
    qid = q["id"]
    st.markdown(f"<div class='hp-card'><b>Q{idx+1}/{TOTAL_Q}</b> — "
                f"<span class='hp-badge'>{q.get('section','Descriptive')}</span></div>", unsafe_allow_html=True)

    if is_mcq(idx):
        sel = st.radio(q["question"], q["options"], index=None, key=f"q_{qid}")
        return sel
    else:
        txt = st.text_area(q["prompt"], key=f"q_{qid}", height=140)
        return txt

def lock_and_next(idx: int, val):
    qid = ALL_QUESTIONS[idx]["id"]
    if val in [None, ""] and is_mcq(idx):
        st.warning("Please select an option before locking.")
        return
    # save answer
    st.session_state.answers[qid] = val
    st.session_state.lock_map[qid] = True
    # move
    if idx+1 < TOTAL_Q:
        st.session_state.index = idx+1
    else:
        submit_and_finish()

def submit_and_finish():
    # compute MCQ score
    mcq_score = 0
    for i, q in enumerate(MCQ_QUESTIONS):
        sel = st.session_state.answers.get(q["id"])
        if sel == q["answer"]:
            mcq_score += MCQ_MARKS
    # descriptive via keyword coverage
    long_total = 0
    for q in LONG_QUESTIONS:
        text = (st.session_state.answers.get(q["id"]) or "").lower()
        hits = [kw for kw in q["keywords"] if kw.lower() in text]
        frac = min(1.0, len(hits) / max(3, len(q["keywords"])//2))
        long_total += int(round(frac * LONG_MARKS))

    total = mcq_score + long_total
    result = "PASS ✅" if total >= PASS_MARK else "FAIL ❌"

    cand = st.session_state.get("cand", {})
    row = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "name": cand.get("name",""),
        "employee_id": cand.get("employee_id",""),
        "mobile": cand.get("mobile",""),
        "email": cand.get("email",""),
        "mcq_score": mcq_score,
        "long_score": long_total,
        "total": total,
        "result": result,
        "warnings": 1 if st.session_state.warned else 0,
    }
    # store answers
    for q in MCQ_QUESTIONS:
        row[f"{q['id']}_sel"] = st.session_state.answers.get(q["id"], "")
    for q in LONG_QUESTIONS:
        row[f"{q['id']}_ans"] = st.session_state.answers.get(q["id"], "")

    try:
        df_old = pd.read_csv(DATA_FILE)
        df_new = pd.concat([df_old, pd.DataFrame([row])], ignore_index=True)
    except Exception:
        df_new = pd.DataFrame([row])
    df_new.to_csv(DATA_FILE, index=False)

    st.success(f"✅ Submitted! MCQ: {mcq_score}  •  Descriptive: {long_total}  •  Total: {total}  •  {result}")
    st.download_button("⬇️ Download your submission (CSV row)", data=pd.DataFrame([row]).to_csv(index=False),
                       file_name=f"{cand.get('employee_id','')}_{cand.get('name','').replace(' ','_')}_submission.csv",
                       mime="text/csv")
    st.stop()

# ---------- MAIN FLOW ----------
if st.session_state.started:
    idx = st.session_state.index

    # show previous locked question (blurred) for context line only
    if idx > 0:
        prev_id = ALL_QUESTIONS[idx-1]["id"]
        st.markdown("<div class='hp-card hp-blur'>Previous question locked.</div>", unsafe_allow_html=True)

    # render current
    val = render_question(idx)

    cols = st.columns([1,1,1])
    with cols[0]:
        st.button("🔒 Lock & Next", type="primary", on_click=lock_and_next, args=(idx, val))
    with cols[1]:
        st.button("Submit Now", on_click=submit_and_finish)
    with cols[2]:
        st.write(f"**Question {idx+1} of {TOTAL_Q}**")

st.markdown("---")
st.subheader("🔐 Admin Panel")
ak = st.text_input("Enter Admin Key", type="password")
if ak == ADMIN_KEY:
    st.success("Access granted.")
    try:
        df = pd.read_csv(DATA_FILE)
        st.dataframe(df, use_container_width=True, height=420)
        st.download_button("⬇️ Download all submissions (CSV)", df.to_csv(index=False),
                           file_name="secure_submissions.csv", mime="text/csv")
    except FileNotFoundError:
        st.info("No submissions yet.")
elif ak:
    st.error("Invalid admin key.")

