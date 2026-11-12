import pandas as pd

from ml_platform.preprocessing.quality.analyzer import QualityAnalyzer


def test_analyzer_detects_outliers_with_iqr():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, 102, 104, 106, 108, 10000],
        }
    )

    report = QualityAnalyzer().analyze(dataframe)

    assert report.outliers["ventas"] >= 1


def test_analyzer_reports_zero_outliers_on_clean_data():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, 102, 104, 106, 108],
        }
    )

    report = QualityAnalyzer().analyze(dataframe)

    assert report.outliers["ventas"] == 0
