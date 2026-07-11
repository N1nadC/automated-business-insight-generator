import pandas as pd


def load_dataset(uploaded_file):
    """
    Load a CSV or Excel file into a Pandas DataFrame.

    Parameters
    ----------
    uploaded_file : UploadedFile

    Returns
    -------
    pd.DataFrame
    """

    if uploaded_file is None:
        return None

    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif filename.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    else:
        raise ValueError("Unsupported file format.")

    return df