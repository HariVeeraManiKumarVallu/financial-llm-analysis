import pandas as pd


def compute_statistics(df):
    """
    Generate descriptive statistics for financial dataset.
    """
    return df.describe()


def sector_analysis(df):
    """
    Compute sector-level return averages.
    """
    return df.groupby("sector")["return"].mean()


def risk_return_analysis(df):
    """
    Evaluate relationship between risk and return.
    """
    correlation = df["return"].corr(df["risk"])
    return correlation