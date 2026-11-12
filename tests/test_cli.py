from pathlib import Path

from typer.testing import CliRunner

from ml_platform.cli import app

runner = CliRunner()


def test_cli_ingest_shows_columns(tmp_path: Path) -> None:
    csv = tmp_path / "ventas.csv"
    csv.write_text(
        "fecha,producto,ventas,costos\n2026-01-01,A,1000,600\n2026-01-02,B,1500,900\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["ingest", str(csv)])

    assert result.exit_code == 0
    assert "ventas" in result.stdout
    assert "costos" in result.stdout


def test_cli_analyze_computes_metrics(tmp_path: Path) -> None:
    csv = tmp_path / "ventas.csv"
    csv.write_text(
        "ventas,costos\n1000,600\n1500,900\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["analyze", str(csv)])

    assert "2,500.00" in result.stdout
    assert "1,500.00" in result.stdout
    assert "1,000.00" in result.stdout
    assert "40.00" in result.stdout


def test_cli_export_csv(tmp_path: Path) -> None:
    csv = tmp_path / "ventas.csv"
    csv.write_text(
        "ventas,costos\n1000,600\n1500,900\n",
        encoding="utf-8",
    )
    output = tmp_path / "out.csv"

    result = runner.invoke(
        app,
        ["export", str(csv), "--output", str(output), "--format", "csv"],
    )

    assert result.exit_code == 0
    assert output.exists()


def test_cli_analyze_fails_without_sales_column(tmp_path: Path) -> None:
    csv = tmp_path / "ventas.csv"
    csv.write_text(
        "producto,precio\nA,100\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["analyze", str(csv)])

    assert result.exit_code == 1
