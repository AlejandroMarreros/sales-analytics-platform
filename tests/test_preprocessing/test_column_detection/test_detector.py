import pandas as pd

from ml_platform.preprocessing.column_detection.detector import ColumnDetector


def test_detector_recognizes_exact_spanish_columns():
    dataframe = pd.DataFrame(columns=["fecha", "ventas", "costos"])

    result = ColumnDetector().detect(dataframe)

    assert result.valid is True
    assert result.get_concept("fecha") == "fecha"
    assert result.get_concept("ventas") == "ventas"
    assert result.get_concept("costos") == "costos"


def test_detector_recognizes_english_columns():
    dataframe = pd.DataFrame(columns=["date", "sales", "costs", "product"])

    result = ColumnDetector().detect(dataframe)

    assert result.get_concept("date") == "fecha"
    assert result.get_concept("sales") == "ventas"
    assert result.get_concept("costs") == "costos"
    assert result.get_concept("product") == "producto"


def test_detector_recognizes_compound_names():
    dataframe = pd.DataFrame(columns=["Total Sales", "Total Costs"])

    result = ColumnDetector().detect(dataframe)

    assert result.get_concept("Total Sales") == "ventas"
    assert result.get_concept("Total Costs") == "costos"


def test_detector_handles_case_and_separators():
    dataframe = pd.DataFrame(columns=["TOTAL_SALES", "total-costs"])

    result = ColumnDetector().detect(dataframe)

    assert result.get_concept("TOTAL_SALES") == "ventas"
    assert result.get_concept("total-costs") == "costos"


def test_detector_handles_accents():
    dataframe = pd.DataFrame(columns=["Área", "Empleado"])

    result = ColumnDetector().detect(dataframe)

    assert result.get_concept("Área") == "area"
    assert result.get_concept("Empleado") == "empleado"


def test_detector_reports_unknown_columns():
    dataframe = pd.DataFrame(columns=["cliente", "xyz"])

    result = ColumnDetector().detect(dataframe)

    assert result.get_concept("cliente") is None
    assert result.get_concept("xyz") is None
    assert result.get_match_type("xyz") == "unknown"


def test_detector_does_not_modify_dataframe():
    dataframe = pd.DataFrame({"Sales": [100, 200]})
    original_columns = dataframe.columns.tolist()
    original_values = dataframe["Sales"].tolist()

    ColumnDetector().detect(dataframe)

    assert dataframe.columns.tolist() == original_columns
    assert dataframe["Sales"].tolist() == original_values


def test_detector_rejects_non_dataframe():
    try:
        ColumnDetector().detect(["ventas", "costos"])
    except TypeError as error:
        assert "DataFrame" in str(error)
    else:
        raise AssertionError("Expected TypeError")


def test_detector_handles_non_string_column_names_as_unknown():
    dataframe = pd.DataFrame({1: [100], "ventas": [200]})

    result = ColumnDetector().detect(dataframe)

    assert result.get_concept(1) is None
    assert result.get_match_type(1) == "unknown"
    assert result.get_concept("ventas") == "ventas"
