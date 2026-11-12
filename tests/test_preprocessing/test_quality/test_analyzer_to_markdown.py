import pandas as pd

from ml_platform.preprocessing.quality.analyzer import QualityAnalyzer


def test_analyzer_to_markdown_returns_table():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, 200, 300],
            "costos": [50, 60, None],
        }
    )

    report = QualityAnalyzer().analyze(dataframe)
    markdown = report.to_markdown()

    assert "|" in markdown
    assert "ventas" in markdown
    assert "costos" in markdown
