from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class CleaningResult:
    dataframe: pd.DataFrame
    rows_dropped: int = 0
    dropped_reasons: tuple[str, ...] = ()

    @property
    def valid(self) -> bool:
        return True
