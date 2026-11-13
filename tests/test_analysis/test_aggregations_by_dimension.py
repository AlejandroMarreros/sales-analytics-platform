import pandas as pd

from ml_platform.analysis.aggregations import aggregate_by_dimension


def test_aggregate_by_area():
    dataframe = pd.DataFrame(
        {
            "area": ["A", "A", "B"],
            "ventas": [100, 200, 300],
            "costos": [50, 80, 100],
        }
    )

    result = aggregate_by_dimension(dataframe, dimension="area")

    assert len(result) == 2
    assert "area" in result.columns
    assert "ventas" in result.columns
    assert "utilidad" in result.columns
    assert "margen" in result.columns


def test_aggregate_by_producto():
    dataframe = pd.DataFrame(
        {
            "producto": ["X", "X", "Y"],
            "ventas": [100, 200, 300],
            "costos": [50, 80, 100],
        }
    )

    result = aggregate_by_dimension(dataframe, dimension="producto")

    assert len(result) == 2
    assert "producto" in result.columns


def test_aggregate_by_dimension_raises_with_missing_column():
    dataframe = pd.DataFrame({"ventas": [100]})

    try:
        aggregate_by_dimension(dataframe, dimension="area")
    except ValueError as exc:
        assert "area" in str(exc).lower()
    else:
        raise AssertionError("Debería lanzar ValueError sin columna 'area'")
