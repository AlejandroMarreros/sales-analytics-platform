import pandas as pd
import pytest

from ml_platform.preprocessing.validation.rules import (
    validate_dataframe_not_empty,
    validate_dataframe_type,
    validate_unique_columns,
)


def test_validate_dataframe_type_accepts_dataframe():
    dataframe = pd.DataFrame({"ventas": [100, 200]})

    assert validate_dataframe_type(dataframe) is None


@pytest.mark.parametrize("value", [None, [], {}, "data", 123])
def test_validate_dataframe_type_rejects_non_dataframe(value):
    with pytest.raises(TypeError):
        validate_dataframe_type(value)


def test_validate_dataframe_not_empty_accepts_dataframe_with_rows():
    dataframe = pd.DataFrame({"ventas": [100]})

    assert validate_dataframe_not_empty(dataframe) is None


def test_validate_dataframe_not_empty_rejects_empty_dataframe():
    dataframe = pd.DataFrame()

    with pytest.raises(ValueError):
        validate_dataframe_not_empty(dataframe)


def test_validate_unique_columns_accepts_unique_columns():
    dataframe = pd.DataFrame(columns=["fecha", "ventas", "costos"])

    assert validate_unique_columns(dataframe) is None


def test_validate_unique_columns_rejects_duplicate_columns():
    dataframe = pd.DataFrame([[1, 2]], columns=["ventas", "ventas"])

    with pytest.raises(ValueError):
        validate_unique_columns(dataframe)
