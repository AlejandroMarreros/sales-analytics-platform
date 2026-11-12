import pandas as pd

from ml_platform.preprocessing.validation.result import ValidationResult
from ml_platform.preprocessing.validation.rules import (
    validate_dataframe_not_empty,
    validate_dataframe_type,
    validate_missing_values,
    validate_numeric_columns,
    validate_required_columns,
    validate_unique_columns,
)


class Validator:
    def __init__(
        self,
        required_columns: tuple[str, ...] = (),
        numeric_columns: tuple[str, ...] = (),
    ) -> None:
        self._required_columns = tuple(required_columns)
        self._numeric_columns = tuple(numeric_columns)

    def validate(self, dataframe: pd.DataFrame) -> ValidationResult:
        validate_dataframe_type(dataframe)

        errors: list[str] = []

        try:
            validate_dataframe_not_empty(dataframe)
        except ValueError as error:
            errors.append(str(error))

        try:
            validate_unique_columns(dataframe)
        except ValueError as error:
            errors.append(str(error))

        errors.extend(
            validate_required_columns(
                dataframe,
                self._required_columns,
            )
        )

        errors.extend(
            validate_numeric_columns(
                dataframe,
                self._numeric_columns,
            )
        )

        warnings = validate_missing_values(dataframe)

        return ValidationResult(
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
