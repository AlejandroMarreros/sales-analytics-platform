from pathlib import Path

import pandas as pd
import typer

from ml_platform.ingestion.reader_factory import ReaderFactory
from ml_platform.preprocessing.cleaning.cleaner import Cleaner
from ml_platform.preprocessing.column_detection.detector import ColumnDetector
from ml_platform.preprocessing.normalization.normalizer import Normalizer
from ml_platform.preprocessing.quality.analyzer import QualityAnalyzer

FORBIDDEN_OUTPUT_PATHS = (
    "/etc",
    "/usr",
    "/boot",
    "/sys",
    "/proc",
    "/dev",
    "/var/lib",
)

app = typer.Typer(
    help="Plataforma modular para ingestión, validación, limpieza y análisis de ventas.",
    no_args_is_help=True,
)


def _check_output_path(output: Path) -> None:
    resolved = output.resolve()
    for forbidden in FORBIDDEN_OUTPUT_PATHS:
        if str(resolved).startswith(forbidden):
            raise ValueError(
                f"No se puede exportar a {forbidden} (path resuelto: {resolved})"
            )


def _load_and_prepare(path: Path) -> pd.DataFrame:
    reader = ReaderFactory.create(path)
    dataframe = reader.read(path)
    detection = ColumnDetector().detect(dataframe)
    normalized = Normalizer().normalize(dataframe, detection)
    cleaned = Cleaner().clean(normalized.dataframe)
    return cleaned.dataframe


@app.command()
def ingest(path: Path) -> None:
    """Lee un archivo y muestra las columnas detectadas."""
    reader = ReaderFactory.create(path)
    dataframe = reader.read(path)
    detection = ColumnDetector().detect(dataframe)

    typer.echo(f"Archivo: {path}")
    typer.echo(f"Filas: {len(dataframe)}")
    typer.echo(f"Columnas: {list(dataframe.columns)}")
    typer.echo("Detección:")
    for match in detection.matches:
        typer.echo(
            f"  {match.column!r} -> {match.concept or 'desconocido'} "
            f"({match.match_type}, confianza {match.confidence})"
        )


@app.command()
def analyze(path: Path) -> None:
    """Calcula métricas básicas: ventas, costos, utilidad y margen."""
    dataframe = _load_and_prepare(path)

    if "ventas" not in dataframe.columns:
        typer.echo("No se detectó la columna 'ventas'. No se puede analizar.")
        raise typer.Exit(code=1)

    total_ventas = float(dataframe["ventas"].sum())
    total_costos = (
        float(dataframe["costos"].sum()) if "costos" in dataframe.columns else 0.0
    )
    utilidad = total_ventas - total_costos
    margen = (utilidad / total_ventas * 100) if total_ventas else 0.0

    typer.echo(f"Archivo: {path}")
    typer.echo(f"Filas analizadas: {len(dataframe)}")
    typer.echo(f"Ventas totales: {total_ventas:,.2f}")
    typer.echo(f"Costos totales: {total_costos:,.2f}")
    typer.echo(f"Utilidad: {utilidad:,.2f}")
    typer.echo(f"Margen: {margen:.2f}%")


@app.command()
def quality(path: Path) -> None:
    """Analiza la calidad del archivo: nulos, cardinalidad, outliers."""
    reader = ReaderFactory.create(path)
    dataframe = reader.read(path)
    report = QualityAnalyzer().analyze(dataframe)

    typer.echo(f"Archivo: {path}")
    typer.echo(report.to_markdown())


@app.command()
def export(
    path: Path,
    output: Path = typer.Option(..., "--output", "-o", help="Archivo de salida"),
    fmt: str = typer.Option("parquet", "--format", "-f", help="parquet | csv"),
) -> None:
    """Exporta el DataFrame limpio a Parquet o CSV."""
    dataframe = _load_and_prepare(path)

    _check_output_path(output)

    if fmt == "parquet":
        dataframe.to_parquet(output, index=False)
    elif fmt == "csv":
        dataframe.to_csv(output, index=False, encoding="utf-8")
    else:
        typer.echo(f"Formato no soportado: {fmt}")
        raise typer.Exit(code=1)

    typer.echo(f"Exportado: {output} ({len(dataframe)} filas, formato {fmt})")


if __name__ == "__main__":
    app()
