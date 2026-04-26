import streamlit as st
from pathlib import Path
import csv
from datetime import datetime

st.set_page_config(page_title="Homework Submission Tracker", page_icon="📘")

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "list" / "HW_LIST.csv"

HEADERS = ["Date", "Level", "Subject", "Homework", "Student"]

with tab1:
    col_title, col_btn = st.columns([6, 1])

    with col_title:
        st.subheader("Find Records")

    with col_btn:
        if "show_filters" not in st.session_state:
            st.session_state.show_filters = False

        if st.button("🔎", key="filter_button"):
            st.session_state.show_filters = not st.session_state.show_filters

    if records:
        levels = sorted(set(r["Level"] for r in records if r["Level"]))
        subjects = sorted(set(r["Subject"] for r in records if r["Subject"]))
        homework_list = sorted(set(r["Homework"] for r in records if r["Homework"]))

        selected_level = "All"
        selected_subject = "All"
        selected_homework = "All"
        student_search = ""

        if st.session_state.show_filters:
            with st.container(border=True):
                st.write("🔎 Filters")

                selected_level = st.selectbox("Filter by Level", ["All"] + levels)
                selected_subject = st.selectbox("Filter by Subject", ["All"] + subjects)
                selected_homework = st.selectbox("Filter by Homework", ["All"] + homework_list)
                student_search = st.text_input("Search student name")

        filtered = records

        if selected_level != "All":
            filtered = [r for r in filtered if r["Level"] == selected_level]

        if selected_subject != "All":
            filtered = [r for r in filtered if r["Subject"] == selected_subject]

        if selected_homework != "All":
            filtered = [r for r in filtered if r["Homework"] == selected_homework]

        if student_search.strip():
            filtered = [
                r for r in filtered
                if student_search.lower() in r["Student"].lower()
            ]

        st.write(f"Showing {len(filtered)} record(s)")

        grouped = {}

        for r in filtered:
            key = f"{r['Level']} | {r['Subject']} | {r['Homework']}"
            grouped.setdefault(key, []).append(r)

        sorted_groups = sorted(
            grouped.items(),
            key=lambda x: (
                -int(x[0].split("|")[0].strip().replace("Primary ", "")),
                x[1][0]["Date"]
            )
        )

        col1, col2 = st.columns(2)

        for i, (group, items) in enumerate(sorted_groups):
            target_col = col1 if i % 2 == 0 else col2

            items = sorted(items, key=lambda x: x["Date"])

            with target_col:
                with st.expander(group, expanded=True):
                    for item in items:
                        st.write(f"- {item['Student']}  |  Added on: {item['Date']}")

    else:
        st.info("No records found yet.")
