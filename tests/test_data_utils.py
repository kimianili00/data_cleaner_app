import pandas as pd
import numpy as np
import pytest
from src.data_utils import handle_missing_values, transform_columns


# ---------- handle_missing_values ----------

def test_no_change_returns_same_df():
    df = pd.DataFrame({"a": [1, np.nan, 3]})
    result = handle_missing_values(df, "no_change")
    assert result.equals(df), "DataFrame should remain unchanged when method=no_change"


def test_fill_with_zero():
    df = pd.DataFrame({"a": [1, np.nan, 3]})
    result = handle_missing_values(df, "zero")
    assert result["a"].isna().sum() == 0
    assert (result["a"] == [1, 0, 3]).all()


def test_fill_with_mean_and_median():
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [10, 20, np.nan]})
    mean_result = handle_missing_values(df, "mean")
    median_result = handle_missing_values(df, "median")

    assert mean_result.isna().sum().sum() == 0
    assert median_result.isna().sum().sum() == 0
    assert list(mean_result.columns) == list(df.columns)
    assert mean_result.shape == df.shape
   


def test_drop_removes_rows():
    df = pd.DataFrame({"a": [1, np.nan, 3]})
    result = handle_missing_values(df, "drop")
    assert len(result) == 2
    assert not result.isna().any().any()


def test_empty_df_returns_itself():
    df = pd.DataFrame()
    result = handle_missing_values(df, "mean")
    assert result.empty


# ---------- transform_columns ----------

def test_normalize_selected_columns():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [10, 20, 30]})
    result = transform_columns(df.copy(), ["x"], "normalize")

    assert np.isclose(result["x"].min(), 0)
    assert np.isclose(result["x"].max(), 1)
    assert result["y"].equals(df["y"]), "Non-selected columns must remain unchanged"


def test_standardize_selected_columns():
    df = pd.DataFrame({"x": [1, 2, 3]})
    result = transform_columns(df, ["x"], "standardize")

    mean, std = result["x"].mean(), result["x"].std(ddof=0)
    assert np.isclose(mean, 0, atol=1e-7)
    assert np.isclose(std, 1, atol=1e-7)


def test_ignore_nonexistent_or_non_numeric_cols():
    df = pd.DataFrame({"x": [1, 2, 3], "y": ["a", "b", "c"]})
    result = transform_columns(df, ["z", "y"], "normalize")
    assert result.equals(df), "Non-numeric or missing columns should be ignored"


def test_empty_input_df():
    df = pd.DataFrame()
    result = transform_columns(df, ["x"], "normalize")
    assert result.empty
