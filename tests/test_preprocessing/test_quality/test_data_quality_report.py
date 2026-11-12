from ml_platform.preprocessing.quality.report import DataQualityReport


def test_report_is_valid_with_defaults():
    report = DataQualityReport(
        rows=10,
        columns=2,
        null_rates={"ventas": 0.0, "costos": 10.0},
        cardinality={"ventas": 10, "costos": 9},
        dtypes={"ventas": "int64", "costos": "int64"},
        outliers={"ventas": 0, "costos": 1},
    )

    assert report.rows == 10
    assert report.columns == 2


def test_report_does_not_expose_mutable_collections():
    report = DataQualityReport(
        rows=1,
        columns=1,
        null_rates={"a": 0.0},
        cardinality={"a": 1},
        dtypes={"a": "int64"},
        outliers={"a": 0},
    )

    assert isinstance(report.null_rates, dict)
    assert isinstance(report.cardinality, dict)
    assert isinstance(report.dtypes, dict)
    assert isinstance(report.outliers, dict)
