import pandas as pd

from ml_platform.preprocessing.cleaning.cleaner import Cleaner


def test_cleaner_drops_rows_with_negative_sales():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, -50, 300],
            "costos": [50, 80, 90],
        }
    )

    result = Cleaner(null_strategy="keep").clean(dataframe)

    assert len(result.dataframe) == 2
    assert result.rows_dropped == 1
    assert any("ventas" in reason for reason in result.dropped_reasons)


def test_cleaner_drops_rows_with_negative_costs():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, 200, 300],
            "costos": [50, -10, 90],
        }
    )

    result = Cleaner(null_strategy="keep").clean(dataframe)

    assert len(result.dataframe) == 2
    assert result.rows_dropped == 1
    assert any("costos" in reason for reason in result.dropped_reasons)


def test_cleaner_keeps_negatives_when_disabled():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, -50, 300],
            "costos": [50, 80, 90],
        }
    )

    result = Cleaner(
        null_strategy="keep",
        drop_negative_sales=False,
    ).clean(dataframe)

    assert len(result.dataframe) == 3
    assert result.rows_dropped == 0
