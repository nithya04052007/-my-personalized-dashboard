import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# App Config
st.set_page_config(page_title="My Personalized Dashboard", layout="wide")

# Storage
DATA_FILE = "college_v12_data.json"
UPLOAD_DIR = "my_uploaded_docs"
if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {
        "subjects": ["Sub 1", "Sub 2", "Sub 3", "Sub 4", "Sub 5", "Sub 6"],
        "exams": {},
        "timetable": [{"Time": "09:00", "Mon": "", "Tue": "", "Wed": "", "Thu": "", "Fri": ""}]
    }

data = load_data()

st.title("🚀 My Personalized Dashboard")

# Subject Editing
with st.expander("📝 Edit Subject Names"):
    c = st.columns(3)
    for i in range(6):
        data["subjects"][i] = c[i%3].text_input(f"Subject {i+1}", data["subjects"][i], key=f"s_{i}")
    if st.button("Save All Settings"):
        with open(DATA_FILE, "w") as f: json.dump(data, f)
        st.success("Saved!")

# Tabs
t1, t2, t3, t4 = st.tabs(["📚 Materials", "📅 Timetable", "📝 Exams", "🎯 Study Hub"])

with t1:
    st.header("Materials Storage")
    sel = st.selectbox("Select Subject", data["subjects"])
    uploaded_files = st.file_uploader(f"Upload for {sel}", accept_multiple_files=True)
    if st.button("Save Files Permanently"):
        if uploaded_files:
            for f_in in uploaded_files:
                with open(os.path.join(UPLOAD_DIR, f_in.name), "wb") as f_out:
                    f_out.write(f_in.getbuffer())
            st.success("Files saved!")
    st.write("📂 Stored Files:", os.listdir(UPLOAD_DIR))

with t2:
    st.header("📅 Weekly Timetable")
    df = pd.DataFrame(data["timetable"])
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    if st.button("Save Timetable"):
        data["timetable"] = edited_df.to_dict('records')
        with open(DATA_FILE, "w") as f: json.dump(data, f)
        st.success("Timetable Saved!")

with t3:
    st.header("⏳ Exam Countdown")
    c1, c2 = st.columns(2)
    with c1:
        ex_sub = st.selectbox("Exam Subject", data["subjects"])
        ex_date = st.date_input("Date", min_value=date.today())
        if st.button("Fix Exam"):
            data["exams"][ex_sub] = str(ex_date)
            with open(DATA_FILE, "w") as f: json.dump(data, f)
    with c2:
        for sub, d_str in data["exams"].items():
            days = (date.fromisoformat(d_str) - date.today()).days
            st.metric(f"{sub} Exam", f"{max(0, days)} Days Left")

with t4:
    st.header("🎯 Study Goals")
    with st.form("goal_form"):
        task = st.text_input("New Goal:")
        t_time = st.time_input("Target Time")
        if st.form_submit_button("Set Goal"):
            st.success(f"Goal Fixed: {task}")