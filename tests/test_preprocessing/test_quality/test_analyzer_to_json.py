import json

import pandas as pd

from ml_platform.preprocessing.quality.analyzer import QualityAnalyzer


def test_analyzer_to_json_returns_valid_json():
    dataframe = pd.DataFrame(
        {
            "ventas": [100, 200, 300],
            "costos": [50, 60, None],
        }
    )

    report = QualityAnalyzer().analyze(dataframe)
    raw = report.to_json()

    parsed = json.loads(raw)

    assert parsed["rows"] == 3
    assert parsed["columns"] == 2
    assert "ventas" in parsed["null_rates"]
