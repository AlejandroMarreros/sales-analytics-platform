import pandas as pd

from ml_platform.preprocessing.cleaning.result import CleaningResult


class Cleaner:
    def __init__(
        self,
        key_columns: tuple[str, ...] = ("ventas", "costos", "fecha"),
        null_strategy: str = "drop",
        drop_duplicates: bool = True,
        drop_negative_sales: bool = True,
        drop_invalid_dates: bool = True,
    ) -> None:
        self._key_columns = key_columns
        self._null_strategy = null_strategy
        self._drop_duplicates = drop_duplicates
        self._drop_negative_sales = drop_negative_sales
        self._drop_invalid_dates = drop_invalid_dates

    def clean(self, dataframe: pd.DataFrame) -> CleaningResult:
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("clean() espera un pandas.DataFrame")

        cleaned = dataframe.copy()
        reasons: list[str] = []
        total_dropped = 0

        # 1. Duplicados exactos
        if self._drop_duplicates:
            before = len(cleaned)
            cleaned = cleaned.drop_duplicates()
            dropped = before - len(cleaned)
            if dropped > 0:
                reasons.append(f"{dropped} filas duplicadas")
                total_dropped += dropped

        # 2. Nulos en columnas clave
        if self._null_strategy != "keep":
            present_keys = [c for c in self._key_columns if c in cleaned.columns]
            if present_keys:
                if self._null_strategy == "drop":
                    before = len(cleaned)
                    cleaned = cleaned.dropna(subset=present_keys)
                    dropped = before - len(cleaned)
                    if dropped > 0:
                        reasons.append(f"{dropped} filas con nulos en columnas clave")
                        total_dropped += dropped
                elif self._null_strategy == "zero":
                    for col in present_keys:
                        if pd.api.types.is_numeric_dtype(cleaned[col]):
                            cleaned[col] = cleaned[col].fillna(0)

        # 3. Fechas inválidas
        if (
            self._drop_invalid_dates
            and "fecha" in cleaned.columns
            and pd.api.types.is_datetime64_any_dtype(cleaned["fecha"])
        ):
            before = len(cleaned)
            cleaned = cleaned.dropna(subset=["fecha"])
            dropped = before - len(cleaned)
            if dropped > 0:
                reasons.append(f"{dropped} filas con fecha inválida")
                total_dropped += dropped

        # 4. Ventas/costos negativos
        if self._drop_negative_sales:
            for col in ("ventas", "costos"):
                if col in cleaned.columns and pd.api.types.is_numeric_dtype(
                    cleaned[col]
                ):
                    before = len(cleaned)
                    cleaned = cleaned[cleaned[col].isna() | (cleaned[col] >= 0)]
                    dropped = before - len(cleaned)
                    if dropped > 0:
                        reasons.append(f"{dropped} filas con {col} negativas")
                        total_dropped += dropped

        return CleaningResult(
            dataframe=cleaned,
            rows_dropped=total_dropped,
            dropped_reasons=tuple(reasons),
        )
