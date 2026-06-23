import os
from dotenv import load_dotenv
import streamlit as st
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = (
    st.secrets["DATABASE_URL"]
    if "DATABASE_URL" in st.secrets
    else os.getenv("DATABASE_URL")
)

engine = create_engine(DATABASE_URL)

def get_engine():
    return engine