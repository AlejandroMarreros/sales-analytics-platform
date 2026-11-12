from ml_platform.preprocessing.column_detection.result import (
    ColumnDetectionResult,
    ColumnMatch,
)


def test_column_match_is_immutable():
    match = ColumnMatch(
        column="sales",
        concept="ventas",
        match_type="synonym",
        confidence="high",
    )

    assert match.column == "sales"
    assert match.concept == "ventas"
    assert match.match_type == "synonym"
    assert match.confidence == "high"


def test_detection_result_is_valid_when_no_ambiguous_matches():
    result = ColumnDetectionResult(
        matches=(ColumnMatch("sales", "ventas", "synonym", "high"),)
    )

    assert result.valid is True


def test_detection_result_detects_unknown_columns():
    result = ColumnDetectionResult(
        matches=(ColumnMatch("xyz", None, "unknown", "none"),)
    )

    assert result.valid is True
    assert result.get_concept("xyz") is None


def test_detection_result_detects_ambiguous_matches():
    result = ColumnDetectionResult(
        matches=(ColumnMatch("amount", None, "ambiguous", "low"),)
    )

    assert result.valid is False
    assert result.get_match_type("amount") == "ambiguous"
