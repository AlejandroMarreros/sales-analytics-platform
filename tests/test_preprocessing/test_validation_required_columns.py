import pandas as pd

from ml_platform.preprocessing.validation.rules import validate_required_columns


def test_validate_required_columns_accepts_expected_columns():
    dataframe = pd.DataFrame(
        {
            "fecha": ["2026-01-01"],
            "ventas": [1000],
            "costos": [600],
        }
    )

    errors = validate_required_columns(
        dataframe,
        required_columns=("fecha", "ventas", "costos"),
    )

    assert errors == ()


def test_validate_required_columns_detects_missing_columns():
    dataframe = pd.DataFrame(
        {
            "fecha": ["2026-01-01"],
            "ventas": [1000],
        }
    )

    errors = validate_required_columns(
        dataframe,
        required_columns=("fecha", "ventas", "costos"),
    )

    assert errors
    assert "costos" in errors[0]
