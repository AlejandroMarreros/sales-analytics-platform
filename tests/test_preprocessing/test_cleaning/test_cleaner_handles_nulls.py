import pandas as pd

from ml_platform.preprocessing.cleaning.cleaner import Cleaner


def test_cleaner_drops_rows_with_nulls_in_key_columns_by_default():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, None, 300],
            "costos": [50, 80, None],
        }
    )

    result = Cleaner(null_strategy="drop").clean(dataframe)

    assert len(result.dataframe) == 1
    assert result.rows_dropped == 2
    assert any("nulos" in reason for reason in result.dropped_reasons)


def test_cleaner_keeps_rows_with_nulls_when_strategy_keep():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, None, 300],
            "costos": [50, 80, None],
        }
    )

    result = Cleaner(null_strategy="keep").clean(dataframe)

    assert len(result.dataframe) == 3
    assert result.rows_dropped == 0


def test_cleaner_fills_nulls_with_zero_when_strategy_zero():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, None, 300],
            "costos": [50, 80, None],
        }
    )

    result = Cleaner(null_strategy="zero").clean(dataframe)

    assert len(result.dataframe) == 3
    assert result.dataframe["ventas"].isna().sum() == 0
    assert result.dataframe["costos"].isna().sum() == 0
    assert result.dataframe["ventas"].tolist() == [100, 0, 300]
