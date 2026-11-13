from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class MetricsResult:
    total_ventas: float
    total_costos: float
    utilidad: float
    margen: float
    ticket_promedio: float
    transacciones: int


class SalesMetrics:
    def compute(self, dataframe: pd.DataFrame) -> MetricsResult:
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("compute() espera un pandas.DataFrame")

        if "ventas" not in dataframe.columns:
            raise ValueError("El DataFrame debe contener la columna 'ventas'")

        total_ventas = float(dataframe["ventas"].sum())
        total_costos = (
            float(dataframe["costos"].sum()) if "costos" in dataframe.columns else 0.0
        )
        utilidad = total_ventas - total_costos
        margen = (utilidad / total_ventas * 100) if total_ventas else 0.0
        transacciones = len(dataframe)
        ticket_promedio = (total_ventas / transacciones) if transacciones else 0.0

        return MetricsResult(
            total_ventas=total_ventas,
            total_costos=total_costos,
            utilidad=utilidad,
            margen=margen,
            ticket_promedio=ticket_promedio,
            transacciones=transacciones,
        )
