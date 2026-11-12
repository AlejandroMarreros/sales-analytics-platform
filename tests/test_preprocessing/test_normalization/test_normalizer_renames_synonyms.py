import pandas as pd

from ml_platform.preprocessing.column_detection.detector import ColumnDetector
from ml_platform.preprocessing.normalization.normalizer import Normalizer


def _normalize(dataframe):
    detection = ColumnDetector().detect(dataframe)
    return Normalizer().normalize(dataframe, detection)


def test_normalizer_renames_sales_to_ventas():
    dataframe = pd.DataFrame({"sales": [1000, 2000]})

    result = _normalize(dataframe)

    assert "ventas" in result.dataframe.columns
    assert "sales" not in result.dataframe.columns
    assert ("sales", "ventas") in result.renamed


def test_normalizer_renames_total_costs_to_costos():
    dataframe = pd.DataFrame({"total_costs": [600, 900]})

    result = _normalize(dataframe)

    assert "costos" in result.dataframe.columns
    assert "total_costs" not in result.dataframe.columns
    assert ("total_costs", "costos") in result.renamed


def test_normalizer_keeps_already_canonical_names():
    dataframe = pd.DataFrame({"ventas": [1000, 2000]})

    result = _normalize(dataframe)

    assert "ventas" in result.dataframe.columns
    assert result.renamed == ()
