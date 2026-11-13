import pandas as pd

from ml_platform.analysis.aggregations import aggregate_by_date


def test_aggregate_by_date_daily():
    dataframe = pd.DataFrame(
        {
            "fecha": pd.to_datetime(["2026-01-01", "2026-01-01", "2026-01-02"]),
            "ventas": [100, 200, 300],
            "costos": [50, 80, 100],
        }
    )

    result = aggregate_by_date(dataframe, freq="D")

    assert len(result) == 2
    assert "ventas" in result.columns
    assert "utilidad" in result.columns
    assert "margen" in result.columns


def test_aggregate_by_date_monthly():
    dataframe = pd.DataFrame(
        {
            "fecha": pd.to_datetime(["2026-01-01", "2026-01-15", "2026-02-01"]),
            "ventas": [100, 200, 300],
            "costos": [50, 80, 100],
        }
    )

    result = aggregate_by_date(dataframe, freq="M")

    assert len(result) == 2
    assert result["ventas"].sum() == 600


def test_aggregate_by_date_raises_without_fecha():
    dataframe = pd.DataFrame({"ventas": [100]})

    try:
        aggregate_by_date(dataframe, freq="D")
    except ValueError as exc:
        assert "fecha" in str(exc).lower()
    else:
        raise AssertionError("Debería lanzar ValueError sin columna 'fecha'")
