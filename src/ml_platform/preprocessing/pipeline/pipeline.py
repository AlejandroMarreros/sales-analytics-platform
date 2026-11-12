import pandas as pd

from ml_platform.preprocessing.column_detection.detector import ColumnDetector
from ml_platform.preprocessing.column_detection.result import ColumnDetectionResult
from ml_platform.preprocessing.pipeline.result import PreprocessingResult
from ml_platform.preprocessing.validation.result import ValidationResult
from ml_platform.preprocessing.validation.validator import Validator


class PreprocessingPipeline:
    def __init__(
        self,
        detector: ColumnDetector | None = None,
        validator: Validator | None = None,
    ) -> None:
        self._detector = detector or ColumnDetector()
        self._validator = validator or Validator(
            numeric_columns=("sales", "costs", "ventas", "costos"),
        )

    def process(self, dataframe: pd.DataFrame) -> PreprocessingResult:
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("dataframe must be a pandas DataFrame")

        column_detection: ColumnDetectionResult = self._detector.detect(dataframe)
        validation: ValidationResult = self._validator.validate(dataframe)

        return PreprocessingResult(
            column_detection=column_detection,
            validation=validation,
        )
