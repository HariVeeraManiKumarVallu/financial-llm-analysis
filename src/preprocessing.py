import pandas as pd

def clean_data(df):
    """
    Basic data preprocessing.
    """
    df = df.dropna()

    df["return"] = df["return"].astype(float)
    df["risk"] = df["risk"].astype(float)
    df["volatility"] = df["volatility"].astype(float)

    return df


def save_cleaned_data(df, path):
    df.to_csv(path, index=False)