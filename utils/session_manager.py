# """
# Session Manager — Centralized Streamlit Session State Helpers

# Provides a clean API for storing and retrieving the uploaded dataset
# across all Streamlit pages.
# """

# import streamlit as st
# import pandas as pd


# # --- Constants ---
# DATA_KEY = "uploaded_df"
# METADATA_KEY = "dataset_metadata"


# def initialize_session():
#     """
#     Initializes session state keys if they don't exist.
#     Call this at the top of every page that needs data access.
#     """
#     if DATA_KEY not in st.session_state:
#         st.session_state[DATA_KEY] = None
#     if METADATA_KEY not in st.session_state:
#         st.session_state[METADATA_KEY] = {}


# def set_dataframe(df: pd.DataFrame, metadata: dict = None):
#     """
#     Stores a DataFrame and optional metadata in session state.

#     Parameters
#     ----------
#     df : pandas.DataFrame
#         The uploaded/cleaned dataset.
#     metadata : dict, optional
#         Additional info like filename, upload timestamp, row count.
#     """
#     st.session_state[DATA_KEY] = df.copy()
#     if metadata:
#         st.session_state[METADATA_KEY].update(metadata)
#     st.session_state[METADATA_KEY]["row_count"] = len(df)
#     st.session_state[METADATA_KEY]["column_count"] = len(df.columns)


# def get_dataframe() -> pd.DataFrame | None:
#     """
#     Retrieves the uploaded DataFrame from session state.

#     Returns
#     -------
#     pandas.DataFrame or None
#         The stored dataset, or None if no data has been uploaded.
#     """
#     return st.session_state.get(DATA_KEY, None)


# def has_data() -> bool:
#     """
#     Checks whether a dataset has been uploaded.

#     Returns
#     -------
#     bool
#     """
#     df = get_dataframe()
#     return df is not None and not df.empty


# def get_metadata() -> dict:
#     """
#     Returns metadata about the uploaded dataset.

#     Returns
#     -------
#     dict
#     """
#     return st.session_state.get(METADATA_KEY, {})


# def clear_data():
#     """
#     Clears the uploaded dataset and metadata from session state.
#     """
#     st.session_state[DATA_KEY] = None
#     st.session_state[METADATA_KEY] = {}


# def require_data(message: str = "Please upload a dataset first.") -> pd.DataFrame | None:
#     """
#     Checks for data and displays a warning if none exists.
#     Returns the DataFrame or None.

#     Parameters
#     ----------
#     message : str
#         Warning message to display if no data is found.

#     Returns
#     -------
#     pandas.DataFrame or None
#     """
#     df = get_dataframe()
#     if df is None:
#         st.warning(message)
#         st.info("Go to **Upload Data** page to import your dataset.")
#         return None
#     return df