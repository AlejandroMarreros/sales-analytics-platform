import pandas as pd


def _compute_aggregated(
    grouped: pd.DataFrame,
    dimension_col: str,
) -> pd.DataFrame:
    grouped = grouped.reset_index()
    grouped["utilidad"] = grouped["ventas"] - grouped.get("costos", 0)
    grouped["margen"] = (
        (grouped["utilidad"] / grouped["ventas"] * 100).fillna(0).round(2)
    )
    return grouped


def _normalize_freq(freq: str) -> str:
    """Traduce aliases de frecuencia de pandas 2.x a 3.x."""
    if freq == "M":
        return "ME"
    if freq == "Q":
        return "QE"
    if freq in ("Y", "A"):
        return "YE"
    if freq == "H":
        return "h"
    if freq == "T":
        return "min"
    if freq == "S":
        return "s"
    return freq


def aggregate_by_date(
    dataframe: pd.DataFrame,
    freq: str = "D",
) -> pd.DataFrame:
    """Agrupa ventas/costos/utilidad/margen por fecha (día o mes)."""
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("aggregate_by_date() espera un pandas.DataFrame")

    if "fecha" not in dataframe.columns:
        raise ValueError("El DataFrame debe contener la columna 'fecha'")

    if "ventas" not in dataframe.columns:
        raise ValueError("El DataFrame debe contener la columna 'ventas'")

    data = dataframe.copy()
    data["fecha"] = pd.to_datetime(data["fecha"], errors="coerce")
    data = data.dropna(subset=["fecha"])

    agg: dict[str, str] = {"ventas": "sum"}
    if "costos" in data.columns:
        agg["costos"] = "sum"

    normalized_freq = _normalize_freq(freq)

    grouped = data.set_index("fecha").resample(normalized_freq).agg(agg).reset_index()

    if "costos" not in grouped.columns:
        grouped["costos"] = 0.0

    grouped = _compute_aggregated(grouped, "fecha")
    return grouped


def aggregate_by_dimension(
    dataframe: pd.DataFrame,
    dimension: str,
) -> pd.DataFrame:
    """Agrupa ventas/costos/utilidad/margen por una dimensión
    (area, producto, empleado)."""
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("aggregate_by_dimension() espera un pandas.DataFrame")

    if dimension not in dataframe.columns:
        raise ValueError(f"El DataFrame debe contener la columna '{dimension}'")

    if "ventas" not in dataframe.columns:
        raise ValueError("El DataFrame debe contener la columna 'ventas'")

    agg: dict[str, str] = {"ventas": "sum"}
    if "costos" in dataframe.columns:
        agg["costos"] = "sum"

    grouped = dataframe.groupby(dimension, dropna=False).agg(agg)

    if "costos" not in grouped.columns:
        grouped["costos"] = 0.0

    grouped = _compute_aggregated(grouped, dimension)
    return grouped
