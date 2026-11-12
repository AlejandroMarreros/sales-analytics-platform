import pandas as pd

from ml_platform.preprocessing.validation.rules import validate_numeric_columns


def test_validate_numeric_columns_accepts_numeric_columns():
    dataframe = pd.DataFrame(
        {
            "ventas": [1000, 2000],
            "costos": [600, 1200],
        }
    )

    errors = validate_numeric_columns(
        dataframe,
        numeric_columns=("ventas", "costos"),
    )

    assert errors == ()


def test_validate_numeric_columns_detects_non_numeric_values():
    dataframe = pd.DataFrame(
        {
            "ventas": [1000, "no disponible"],
            "costos": [600, 1200],
        }
    )

    errors = validate_numeric_columns(
        dataframe,
        numeric_columns=("ventas", "costos"),
    )

    assert errors
    assert "ventas" in errors[0]


def test_validate_numeric_columns_ignores_missing_columns():
    dataframe = pd.DataFrame(
        {
            "ventas": [1000, 2000],
        }
    )

    errors = validate_numeric_columns(
        dataframe,
        ("ventas", "costos"),
    )

    assert errors == ()
