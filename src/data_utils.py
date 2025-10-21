import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def handle_missing_values(df: pd.DataFrame, method: str) -> pd.DataFrame:
    """Handle missing values according to the selected strategy."""
    if df.empty:
        return df

    numeric_cols = df.select_dtypes(include=np.number).columns

    if method == "zero":
        df = df.fillna(0)
    elif method == "mean" and len(numeric_cols) > 0:
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif method == "median" and len(numeric_cols) > 0:
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif method == "drop":
        df = df.dropna()

    return df


def transform_columns(df: pd.DataFrame, cols: list[str], method: str) -> pd.DataFrame:
    """Apply scaling transformations to selected numeric columns."""
    if df.empty or not cols:
        return df

    cols = [c for c in cols if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
    if not cols:
        return df

    if method == "normalize":
        scaler = MinMaxScaler()
        df[cols] = scaler.fit_transform(df[cols])
    elif method == "standardize":
        scaler = StandardScaler()
        df[cols] = scaler.fit_transform(df[cols])

    return df
