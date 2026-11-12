from pathlib import Path

import pandas as pd
import pytest

from ml_platform.ingestion.pdf_reader import PDFReader


def test_pdf_reader_reads_valid_pdf():
    file_path = Path("data/raw/ventas_prueba.pdf")

    reader = PDFReader()
    result = reader.read(file_path)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert list(result.columns) == ["page", "text"]
    assert result.iloc[0]["page"] == 1
    assert "Reporte de ventas de prueba" in result.iloc[0]["text"]


def test_pdf_reader_raises_error_when_file_does_not_exist():
    file_path = Path("data/raw/archivo_inexistente.pdf")

    reader = PDFReader()

    with pytest.raises(FileNotFoundError):
        reader.read(file_path)


def test_pdf_reader_raises_error_for_invalid_extension():
    file_path = Path("data/raw/ventas_prueba.txt")

    reader = PDFReader()

    with pytest.raises(ValueError):
        reader.read(file_path)
