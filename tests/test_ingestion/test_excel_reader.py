from pathlib import Path

import pandas as pd
import pytest

from ml_platform.ingestion.excel_reader import ExcelReader


def test_excel_reader_reads_valid_excel():
    file_path = Path("data/raw/ventas_prueba.xlsx")

    reader = ExcelReader()
    result = reader.read(file_path)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert list(result.columns) == ["fecha", "producto", "ventas", "costos"]


def test_excel_reader_raises_error_when_file_does_not_exist():
    file_path = Path("data/raw/archivo_inexistente.xlsx")

    reader = ExcelReader()

    with pytest.raises(FileNotFoundError):
        reader.read(file_path)


def test_excel_reader_raises_error_for_invalid_extension():
    file_path = Path("data/raw/ventas_prueba.txt")

    reader = ExcelReader()

    with pytest.raises(ValueError):
        reader.read(file_path)
