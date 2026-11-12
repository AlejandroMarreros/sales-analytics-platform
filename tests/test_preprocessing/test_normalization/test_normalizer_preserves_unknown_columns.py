import pandas as pd
from ml_platform.preprocessing.normalization.normalizer import Normalizer

from ml_platform.preprocessing.column_detection.detector import ColumnDetector


def _normalize(dataframe):
    detection = ColumnDetector().detect(dataframe)
    return Normalizer().normalize(dataframe, detection)


def test_normalizer_keeps_unknown_columns_untouched():
    dataframe = pd.DataFrame(
        {
            "sales": [1000, 2000],
            "observaciones": ["ok", "revisar"],
        }
    )

    result = _normalize(dataframe)

    assert "ventas" in result.dataframe.columns
    assert "observaciones" in result.dataframe.columns
    assert result.dataframe["observaciones"].tolist() == ["ok", "revisar"]


def test_normalizer_reports_skipped_columns():
    dataframe = pd.DataFrame(
        {
            "sales": [1000, 2000],
            "observaciones": ["ok", "revisar"],
        }
    )

    result = _normalize(dataframe)

    assert "observaciones" in result.skipped
