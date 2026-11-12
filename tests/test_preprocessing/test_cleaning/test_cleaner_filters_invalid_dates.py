import pandas as pd

from ml_platform.preprocessing.cleaning.cleaner import Cleaner


def test_cleaner_drops_rows_with_invalid_dates():
    dataframe = pd.DataFrame(
        {
            "fecha": pd.to_datetime(["2026-01-01", None, "2026-01-03"]),
            "ventas": [100, 200, 300],
            "costos": [50, 80, 90],
        }
    )

    result = Cleaner(null_strategy="keep").clean(dataframe)

    assert len(result.dataframe) == 2
    assert result.rows_dropped == 1
    assert any("fecha" in reason for reason in result.dropped_reasons)


def test_cleaner_keeps_invalid_dates_when_disabled():
    dataframe = pd.DataFrame(
        {
            "fecha": pd.to_datetime(["2026-01-01", None, "2026-01-03"]),
            "ventas": [100, 200, 300],
            "costos": [50, 80, 90],
        }
    )

    result = Cleaner(
        null_strategy="keep",
        drop_invalid_dates=False,
    ).clean(dataframe)

    assert len(result.dataframe) == 3
    assert result.rows_dropped == 0
