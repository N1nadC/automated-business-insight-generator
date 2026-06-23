import streamlit as st

st.set_page_config(
    page_title="Automated Business Insight Generator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Automated Business Insight Generator")

st.markdown("""
### Transform raw business data into automated insights

This application analyzes e-commerce business data and automatically generates:

- 📈 Revenue KPIs
- 📊 Interactive Visualizations
- 🛒 Product Performance Analysis
- 🌎 Regional Analysis
- 👥 Customer Insights
- 🚚 Delivery Performance Metrics
- 🤖 AI-generated Executive Summaries
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tech Stack")

    st.markdown("""
    - Python
    - PostgreSQL (Neon)
    - Pandas
    - SQLAlchemy
    - Plotly
    - Streamlit
    """)

with col2:
    st.subheader("Completed Modules")

    st.markdown("""
    ✅ Analytics Engine

    ✅ Insight Generation Engine

    ✅ KPI Engine

    ✅ Visualization Layer

    ✅ Executive Summary Generator
    """)

st.divider()

st.success("Use the sidebar to explore the dashboard pages.")