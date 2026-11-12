import pandas as pd

from ml_platform.preprocessing.validator import Validator


def test_validator_accepts_valid_dataframe():
    dataframe = pd.DataFrame(
        {
            "fecha": ["2026-01-01"],
            "ventas": [1000],
            "costos": [600],
        }
    )

    result = Validator().validate(dataframe)

    assert result.valid is True
    assert result.errors == ()


def test_validator_rejects_non_dataframe():
    result = Validator().validate("datos")

    assert result.valid is False
    assert result.errors


def test_validator_rejects_empty_dataframe():
    dataframe = pd.DataFrame()

    result = Validator().validate(dataframe)

    assert result.valid is False
    assert result.errors


def test_validator_rejects_duplicate_columns():
    dataframe = pd.DataFrame([[100, 200]], columns=["ventas", "ventas"])

    result = Validator().validate(dataframe)

    assert result.valid is False
    assert result.errors


def test_validator_reports_missing_values_as_warning():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, None],
            "costos": [60, 120],
        }
    )

    result = Validator().validate(dataframe)

    assert result.valid is True
    assert result.errors == ()
    assert result.warnings
    assert "valores faltantes" in result.warnings[0].lower()


def test_validator_rejects_missing_required_columns():
    dataframe = pd.DataFrame(
        {
            "fecha": ["2026-01-01"],
            "ventas": [1000],
        }
    )

    result = Validator().validate(
        dataframe,
        required_columns=("fecha", "ventas", "costos"),
    )

    assert result.valid is False
    assert result.errors
    assert "costos" in result.errors[0]


def test_validator_rejects_non_numeric_values():
    dataframe = pd.DataFrame(
        {
            "fecha": ["2026-01-01", "2026-01-02"],
            "ventas": [1000, "no disponible"],
            "costos": [600, 1200],
        }
    )

    result = Validator().validate(
        dataframe,
        numeric_columns=("ventas", "costos"),
    )

    assert result.valid is False
    assert result.errors
    assert "ventas" in result.errors[0]
