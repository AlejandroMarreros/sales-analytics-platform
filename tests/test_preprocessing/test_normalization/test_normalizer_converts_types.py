import pandas as pd

from ml_platform.preprocessing.column_detection.detector import ColumnDetector
from ml_platform.preprocessing.normalization.normalizer import Normalizer


def _normalize(dataframe):
    detection = ColumnDetector().detect(dataframe)
    return Normalizer().normalize(dataframe, detection)


def test_normalizer_converts_date_column_to_datetime():
    dataframe = pd.DataFrame({"fecha": ["2026-01-01", "2026-01-02"]})

    result = _normalize(dataframe)

    assert pd.api.types.is_datetime64_any_dtype(result.dataframe["fecha"])


def test_normalizer_converts_sales_and_costs_to_numeric():
    dataframe = pd.DataFrame(
        {
            "sales": ["1000", "2000"],
            "costs": ["600", "900"],
        }
    )

    result = _normalize(dataframe)

    assert pd.api.types.is_numeric_dtype(result.dataframe["ventas"])
    assert pd.api.types.is_numeric_dtype(result.dataframe["costos"])
