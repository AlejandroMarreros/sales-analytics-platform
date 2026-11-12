import pandas as pd

from ml_platform.preprocessing.validation.rules import validate_missing_values


def test_validate_missing_values_accepts_complete_dataframe():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, 200],
            "costos": [60, 120],
        }
    )

    warnings = validate_missing_values(dataframe)

    assert warnings == ()


def test_validate_missing_values_detects_missing_values():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, None],
            "costos": [60, 120],
        }
    )

    warnings = validate_missing_values(dataframe)

    assert warnings
    assert "valores faltantes" in warnings[0].lower()
