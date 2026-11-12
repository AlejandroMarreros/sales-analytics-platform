from dataclasses import dataclass

from ml_platform.preprocessing.column_detection.result import ColumnDetectionResult
from ml_platform.preprocessing.validation.result import ValidationResult


@dataclass(frozen=True)
class PreprocessingResult:
    column_detection: ColumnDetectionResult
    validation: ValidationResult

    @property
    def valid(self) -> bool:
        return self.column_detection.valid and self.validation.valid
