import pandas as pd
from ml_platform.preprocessing.normalization.normalizer import Normalizer

from ml_platform.preprocessing.column_detection.detector import ColumnDetector


def test_normalizer_does_not_mutate_input_dataframe():
    dataframe = pd.DataFrame({"sales": [1000, 2000], "costs": [600, 900]})
    columns_before = list(dataframe.columns)

    detection = ColumnDetector().detect(dataframe)
    Normalizer().normalize(dataframe, detection)

    assert list(dataframe.columns) == columns_before
    assert dataframe["sales"].tolist() == [1000, 2000]
    assert dataframe["costs"].tolist() == [600, 900]
