import pandas as pd

def load_financial_data(path: str):
    """
    Load financial dataset from CSV file.
    """
    df = pd.read_csv(path)
    return df