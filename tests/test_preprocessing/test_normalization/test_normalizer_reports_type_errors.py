import pandas as pd
from ml_platform.preprocessing.normalization.normalizer import Normalizer

from ml_platform.preprocessing.column_detection.detector import ColumnDetector


def _normalize(dataframe):
    detection = ColumnDetector().detect(dataframe)
    return Normalizer().normalize(dataframe, detection)


def test_normalizer_reports_non_convertible_numeric_values():
    dataframe = pd.DataFrame({"sales": ["1000", "no disponible"]})

    result = _normalize(dataframe)

    assert result.valid is False
    assert len(result.type_errors) == 1


def test_normalizer_reports_unparseable_dates():
    dataframe = pd.DataFrame({"fecha": ["2026-01-01", "no es fecha"]})

    result = _normalize(dataframe)

    assert result.valid is False
    assert len(result.type_errors) == 1
