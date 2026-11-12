import pandas as pd


def validate_dataframe_type(dataframe: object) -> None:
    """Valida que el valor recibido sea un pandas.DataFrame."""
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("El valor debe ser un pandas.DataFrame")


def validate_dataframe_not_empty(dataframe: pd.DataFrame) -> None:
    """Valida que el DataFrame contenga al menos una fila."""
    if dataframe.empty:
        raise ValueError("El DataFrame no puede estar vacío")


def validate_unique_columns(dataframe: pd.DataFrame) -> None:
    """Valida que el DataFrame no tenga columnas duplicadas."""
    if dataframe.columns.duplicated().any():
        raise ValueError("El DataFrame contiene columnas duplicadas")


def validate_missing_values(dataframe: pd.DataFrame) -> tuple[str, ...]:
    """Detecta valores faltantes y devuelve advertencias."""
    missing_count = int(dataframe.isna().sum().sum())

    if missing_count == 0:
        return ()

    return (f"Se encontraron {missing_count} valores faltantes",)


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: tuple[str, ...],
) -> tuple[str, ...]:
    """Detecta columnas obligatorias ausentes."""
    missing_columns = tuple(
        column for column in required_columns if column not in dataframe.columns
    )

    if not missing_columns:
        return ()

    return (f"Faltan columnas requeridas: {', '.join(missing_columns)}",)


def validate_numeric_columns(
    dataframe: pd.DataFrame,
    numeric_columns: tuple[str, ...],
) -> tuple[str, ...]:
    """Detecta columnas que contienen valores no numéricos."""
    errors: list[str] = []

    for column in numeric_columns:
        if column not in dataframe.columns:
            continue

        converted = pd.to_numeric(dataframe[column], errors="coerce")
        invalid_count = int(converted.isna().sum() - dataframe[column].isna().sum())

        if invalid_count > 0:
            errors.append(
                f"La columna '{column}' contiene {invalid_count} valores no numéricos"
            )

    return tuple(errors)
