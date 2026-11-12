import pandas as pd

from ml_platform.preprocessing.column_detection.detector import ColumnDetector
from ml_platform.preprocessing.column_detection.result import ColumnDetectionResult
from ml_platform.preprocessing.normalization.result import NormalizationResult

_NUMERIC_CONCEPTS = ("ventas", "costos")
_DATE_CONCEPTS = ("fecha",)


class Normalizer:
    def __init__(self, detector: ColumnDetector | None = None) -> None:
        self._detector = detector or ColumnDetector()

    def normalize(
        self,
        dataframe: pd.DataFrame,
        detection: ColumnDetectionResult | None = None,
    ) -> NormalizationResult:
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("normalize() espera un pandas.DataFrame")

        detection = detection or self._detector.detect(dataframe)

        renamed: list[tuple[object, str]] = []
        skipped: list[object] = []
        rename_map: dict[object, str] = {}

        for match in detection.matches:
            if match.concept is None:
                skipped.append(match.column)
                continue
            if match.match_type in ("exact", "synonym"):
                if match.column != match.concept:
                    rename_map[match.column] = match.concept
                    renamed.append((match.column, match.concept))
            else:
                skipped.append(match.column)

        normalized = dataframe.rename(columns=rename_map).copy()

        type_errors: list[str] = []

        for concept in _DATE_CONCEPTS:
            if concept in normalized.columns:
                before = normalized[concept].isna()
                converted = pd.to_datetime(normalized[concept], errors="coerce")
                newly_na = converted.isna() & ~before
                if newly_na.any():
                    type_errors.append(
                        f"{concept} contiene {int(newly_na.sum())} valores de fecha no válidos"
                    )
                normalized[concept] = converted

        for concept in _NUMERIC_CONCEPTS:
            if concept in normalized.columns:
                before = normalized[concept].isna()
                converted = pd.to_numeric(normalized[concept], errors="coerce")
                newly_na = converted.isna() & ~before
                if newly_na.any():
                    type_errors.append(
                        f"{concept} contiene {int(newly_na.sum())} valores no numéricos"
                    )
                normalized[concept] = converted

        return NormalizationResult(
            dataframe=normalized,
            renamed=tuple(renamed),
            type_errors=tuple(type_errors),
            skipped=tuple(skipped),
        )
