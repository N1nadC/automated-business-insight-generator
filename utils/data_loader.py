import os
import pandas as pd

UPLOAD_DIR = "data/uploads"


def save_uploaded_file(uploaded_file):
    """
    Save uploaded CSV to disk.
    Returns the saved file path.
    """

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def load_csv(uploaded_file):
    """
    Save uploaded CSV and return DataFrame.
    """
    file_path = save_uploaded_file(uploaded_file)

    df = pd.read_csv(file_path)

    return df, file_path


def load_saved_dataset(file_path):
    """
    Reload dataset from disk.
    """

    return pd.read_csv(file_path)


def get_dataset_info(df):

    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "memory_mb": round(memory_mb, 2),
    }