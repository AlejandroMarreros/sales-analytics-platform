from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class NormalizationResult:
    dataframe: pd.DataFrame
    renamed: tuple[tuple[object, str], ...] = ()
    type_errors: tuple[str, ...] = ()
    skipped: tuple[object, ...] = ()

    @property
    def valid(self) -> bool:
        return not self.type_errors
