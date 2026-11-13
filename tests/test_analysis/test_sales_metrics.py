import pandas as pd

from ml_platform.analysis.metrics import SalesMetrics


def test_sales_metrics_computes_all_fields():
    dataframe = pd.DataFrame(
        {
            "ventas": [1000, 1500],
            "costos": [600, 900],
        }
    )

    result = SalesMetrics().compute(dataframe)

    assert result.total_ventas == 2500.0
    assert result.total_costos == 1500.0
    assert result.utilidad == 1000.0
    assert result.margen == 40.0
    assert result.ticket_promedio == 1250.0
    assert result.transacciones == 2


def test_sales_metrics_handles_missing_costs_column():
    dataframe = pd.DataFrame({"ventas": [1000, 1500]})

    result = SalesMetrics().compute(dataframe)

    assert result.total_costos == 0.0
    assert result.utilidad == 2500.0
    assert result.margen == 100.0


def test_sales_metrics_handles_zero_sales():
    dataframe = pd.DataFrame({"ventas": [0], "costos": [0]})

    result = SalesMetrics().compute(dataframe)

    assert result.margen == 0.0


def test_sales_metrics_raises_without_sales_column():
    dataframe = pd.DataFrame({"costos": [100]})

    try:
        SalesMetrics().compute(dataframe)
    except ValueError as exc:
        assert "ventas" in str(exc).lower()
    else:
        raise AssertionError("Debería lanzar ValueError sin columna 'ventas'")


def test_sales_metrics_does_not_mutate_input():
    dataframe = pd.DataFrame({"ventas": [100, 200], "costos": [50, 80]})
    original = dataframe.copy()

    SalesMetrics().compute(dataframe)

    pd.testing.assert_frame_equal(dataframe, original)
