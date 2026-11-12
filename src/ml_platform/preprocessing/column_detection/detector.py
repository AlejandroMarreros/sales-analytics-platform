import re
import unicodedata

import pandas as pd

from ml_platform.preprocessing.column_detection.dictionary import COLUMN_DICTIONARY
from ml_platform.preprocessing.column_detection.result import (
    ColumnDetectionResult,
    ColumnMatch,
)


class ColumnDetector:
    def __init__(self, dictionary: dict[str, tuple[str, ...]] | None = None):
        self._dictionary = dictionary or COLUMN_DICTIONARY
        self._index = self._build_index()

    def _build_index(self) -> dict[str, set[str]]:
        index: dict[str, set[str]] = {}

        for concept, aliases in self._dictionary.items():
            for alias in aliases:
                normalized = self._normalize(alias)
                index.setdefault(normalized, set()).add(concept)

        return index

    @staticmethod
    def _normalize(value: str) -> str:
        value = unicodedata.normalize("NFKD", value)
        value = "".join(
            character for character in value if not unicodedata.combining(character)
        )
        value = value.casefold()
        value = re.sub(r"[_-]+", " ", value)
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    def detect(self, dataframe: pd.DataFrame) -> ColumnDetectionResult:
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("dataframe must be a pandas DataFrame")

        matches: list[ColumnMatch] = []

        for column in dataframe.columns:
            if not isinstance(column, str):
                matches.append(
                    ColumnMatch(
                        column=column,
                        concept=None,
                        match_type="unknown",
                        confidence="none",
                    )
                )
                continue

            normalized = self._normalize(column)
            concepts = self._index.get(normalized, set())

            if len(concepts) == 1:
                concept = next(iter(concepts))
                canonical = self._normalize(concept)
                match_type = "exact" if normalized == canonical else "synonym"
                matches.append(
                    ColumnMatch(
                        column=column,
                        concept=concept,
                        match_type=match_type,
                        confidence="high",
                    )
                )
            elif len(concepts) > 1:
                matches.append(
                    ColumnMatch(
                        column=column,
                        concept=None,
                        match_type="ambiguous",
                        confidence="low",
                    )
                )
            else:
                matches.append(
                    ColumnMatch(
                        column=column,
                        concept=None,
                        match_type="unknown",
                        confidence="none",
                    )
                )

        return ColumnDetectionResult(matches=tuple(matches))
