from typing import Any

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
    """Orquesta las reglas básicas de validación de DataFrames."""

    def validate(
        self,
        dataframe: Any,
        required_columns: tuple[str, ...] = (),
        numeric_columns: tuple[str, ...] = (),
    ) -> ValidationResult:
        """Ejecuta las reglas de validación y devuelve su resultado."""
        errors: list[str] = []
        warnings: list[str] = []

        try:
            validate_dataframe_type(dataframe)
        except TypeError as error:
            errors.append(str(error))
            return ValidationResult(errors=tuple(errors))

        try:
            validate_dataframe_not_empty(dataframe)
        except ValueError as error:
            errors.append(str(error))

        try:
            validate_unique_columns(dataframe)
        except ValueError as error:
            errors.append(str(error))

        errors.extend(validate_required_columns(dataframe, required_columns))

        errors.extend(validate_numeric_columns(dataframe, numeric_columns))

        warnings.extend(validate_missing_values(dataframe))

        return ValidationResult(
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
