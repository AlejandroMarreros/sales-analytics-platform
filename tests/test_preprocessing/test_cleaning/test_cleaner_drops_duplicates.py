import pandas as pd

from ml_platform.preprocessing.cleaning.cleaner import Cleaner


def test_cleaner_drops_exact_duplicates():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, 200, 100, 300],
            "costos": [50, 80, 50, 90],
        }
    )

    result = Cleaner(null_strategy="keep").clean(dataframe)

    assert len(result.dataframe) == 3
    assert result.rows_dropped == 1
    assert any("duplicadas" in reason for reason in result.dropped_reasons)


def test_cleaner_keeps_duplicates_when_disabled():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, 200, 100],
            "costos": [50, 80, 50],
        }
    )

    result = Cleaner(
        null_strategy="keep",
        drop_duplicates=False,
    ).clean(dataframe)

    assert len(result.dataframe) == 3
    assert result.rows_dropped == 0
