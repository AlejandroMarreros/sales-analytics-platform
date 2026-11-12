import json
from dataclasses import dataclass


@dataclass(frozen=True)
class DataQualityReport:
    rows: int
    columns: int
    null_rates: dict[str, float]
    cardinality: dict[str, int]
    dtypes: dict[str, str]
    outliers: dict[str, int]

    def to_markdown(self) -> str:
        lines = [
            f"# Reporte de calidad ({self.rows} filas, {self.columns} columnas)",
            "",
            "| Columna | Tipo | % Nulos | Únicos | Outliers |",
            "|---|---|---|---|---|",
        ]
        for col in self.null_rates:
            lines.append(
                f"| {col} | {self.dtypes[col]} | {self.null_rates[col]:.1f}% "
                f"| {self.cardinality[col]} | {self.outliers.get(col, 0)} |"
            )
        return "\n".join(lines)

    def to_json(self) -> str:
        return json.dumps(
            {
                "rows": self.rows,
                "columns": self.columns,
                "null_rates": self.null_rates,
                "cardinality": self.cardinality,
                "dtypes": self.dtypes,
                "outliers": self.outliers,
            },
            indent=2,
        )
