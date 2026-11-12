import pandas as pd

from ml_platform.preprocessing.quality.analyzer import QualityAnalyzer


def test_analyzer_computes_null_rates():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, None, 300, 400],
            "costos": [50, 60, 70, None],
        }
    )

    report = QualityAnalyzer().analyze(dataframe)

    assert report.rows == 4
    assert report.columns == 2
    assert report.null_rates["ventas"] == 25.0
    assert report.null_rates["costos"] == 25.0


def test_analyzer_reports_zero_null_rates():
    dataframe = pd.DataFrame({"ventas": [100, 200, 300]})

    report = QualityAnalyzer().analyze(dataframe)

    assert report.null_rates["ventas"] == 0.0
