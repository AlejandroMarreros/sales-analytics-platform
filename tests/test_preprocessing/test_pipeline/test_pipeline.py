import pandas as pd
import pytest

from ml_platform.preprocessing.pipeline import PreprocessingPipeline


def test_pipeline_accepts_valid_dataframe():
    dataframe = pd.DataFrame(
        {
            "fecha": ["2025-01-01"],
            "ventas": [100],
            "costos": [50],
        }
    )

    result = PreprocessingPipeline().process(dataframe)

    assert result.valid is True
    assert result.column_detection.get_concept("fecha") == "fecha"
    assert result.column_detection.get_concept("ventas") == "ventas"
    assert result.column_detection.get_concept("costos") == "costos"


def test_pipeline_detects_english_columns():
    dataframe = pd.DataFrame(
        {
            "date": ["2025-01-01"],
            "sales": [100],
            "costs": [50],
        }
    )

    result = PreprocessingPipeline().process(dataframe)

    assert result.valid is True
    assert result.column_detection.get_concept("date") == "fecha"
    assert result.column_detection.get_concept("sales") == "ventas"
    assert result.column_detection.get_concept("costs") == "costos"


def test_pipeline_rejects_invalid_dataframe():
    with pytest.raises(TypeError, match="DataFrame"):
        PreprocessingPipeline().process(["ventas", "costos"])


def test_pipeline_preserves_dataframe():
    dataframe = pd.DataFrame(
        {
            "sales": [100, 200],
            "costs": [50, 75],
        }
    )

    original = dataframe.copy(deep=True)

    PreprocessingPipeline().process(dataframe)

    pd.testing.assert_frame_equal(dataframe, original)


def test_pipeline_reports_validation_errors():
    dataframe = pd.DataFrame(
        {
            "sales": ["not numeric"],
            "costs": [50],
        }
    )

    result = PreprocessingPipeline().process(dataframe)

    assert result.valid is False
    assert result.validation.valid is False


def test_pipeline_reports_unknown_columns_without_mutating_data():
    dataframe = pd.DataFrame(
        {
            "sales": [100],
            "customer_name": ["Alice"],
        }
    )

    result = PreprocessingPipeline().process(dataframe)

    assert result.column_detection.get_concept("sales") == "ventas"
    assert result.column_detection.get_concept("customer_name") is None
    assert dataframe.columns.tolist() == ["sales", "customer_name"]
