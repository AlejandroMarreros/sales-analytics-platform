import dataclasses

from ml_platform.analysis.metrics import MetricsResult


def test_metrics_result_holds_values():
    result = MetricsResult(
        total_ventas=2500.0,
        total_costos=1500.0,
        utilidad=1000.0,
        margen=40.0,
        ticket_promedio=1250.0,
        transacciones=2,
    )

    assert result.total_ventas == 2500.0
    assert result.utilidad == 1000.0
    assert result.transacciones == 2


def test_metrics_result_is_frozen():
    result = MetricsResult(
        total_ventas=100.0,
        total_costos=50.0,
        utilidad=50.0,
        margen=50.0,
        ticket_promedio=50.0,
        transacciones=2,
    )

    try:
        result.total_ventas = 200.0
    except dataclasses.FrozenInstanceError:
        pass
    else:
        raise AssertionError("MetricsResult debería ser inmutable")
