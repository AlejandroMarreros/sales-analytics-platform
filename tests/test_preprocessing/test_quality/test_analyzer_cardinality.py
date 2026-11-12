import pandas as pd

from ml_platform.preprocessing.quality.analyzer import QualityAnalyzer


def test_analyzer_computes_cardinality():
    dataframe = pd.DataFrame(
        {
            "producto": ["A", "A", "B", "C"],
            "ventas": [100, 200, 300, 400],
        }
    )

    report = QualityAnalyzer().analyze(dataframe)

    assert report.cardinality["producto"] == 3
    assert report.cardinality["ventas"] == 4
