import streamlit as st

from reports.executive_summary import generate_executive_summary

st.title("AI Business Insights")

summary = generate_executive_summary()

st.text(summary)