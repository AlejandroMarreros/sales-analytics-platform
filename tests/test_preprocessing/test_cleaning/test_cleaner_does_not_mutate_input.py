import pandas as pd

from ml_platform.preprocessing.cleaning.cleaner import Cleaner


def test_cleaner_does_not_mutate_input_dataframe():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, 100, 300],
            "costos": [50, 50, 90],
        }
    )
    original_shape = dataframe.shape
    original_values = dataframe.copy()

    Cleaner(null_strategy="keep").clean(dataframe)

    assert dataframe.shape == original_shape
    pd.testing.assert_frame_equal(dataframe, original_values)


def test_cleaner_does_not_mutate_input_when_nulls_filled_with_zero():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, None, 300],
            "costos": [50, 80, None],
        }
    )
    original_values = dataframe.copy()

    Cleaner(null_strategy="zero").clean(dataframe)

    pd.testing.assert_frame_equal(dataframe, original_values)
