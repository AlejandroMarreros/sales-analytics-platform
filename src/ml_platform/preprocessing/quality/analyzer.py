import pandas as pd

from ml_platform.preprocessing.quality.report import DataQualityReport


class QualityAnalyzer:
    def analyze(self, dataframe: pd.DataFrame) -> DataQualityReport:
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("analyze() espera un pandas.DataFrame")

        rows = len(dataframe)
        columns = len(dataframe.columns)

        null_rates = {
            str(col): float(dataframe[col].isna().mean() * 100)
            for col in dataframe.columns
        }

        cardinality = {
            str(col): int(dataframe[col].nunique(dropna=True))
            for col in dataframe.columns
        }

        dtypes = {str(col): str(dataframe[col].dtype) for col in dataframe.columns}

        outliers: dict[str, int] = {}
        for col in dataframe.columns:
            if pd.api.types.is_numeric_dtype(dataframe[col]):
                series = dataframe[col].dropna()
                if len(series) < 4:
                    outliers[str(col)] = 0
                    continue
                q1 = series.quantile(0.25)
                q3 = series.quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                outliers[str(col)] = int(((series < lower) | (series > upper)).sum())

        return DataQualityReport(
            rows=rows,
            columns=columns,
            null_rates=null_rates,
            cardinality=cardinality,
            dtypes=dtypes,
            outliers=outliers,
        )
