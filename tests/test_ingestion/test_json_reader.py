from pathlib import Path

import pandas as pd
import pytest

from ml_platform.ingestion.json_reader import JSONReader


def test_json_reader_reads_valid_json():
    file_path = Path("data/raw/ventas_prueba.json")

    reader = JSONReader()
    result = reader.read(file_path)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert list(result.columns) == ["fecha", "producto", "ventas", "costos"]


def test_json_reader_raises_error_when_file_does_not_exist():
    file_path = Path("data/raw/archivo_inexistente.json")

    reader = JSONReader()

    with pytest.raises(FileNotFoundError):
        reader.read(file_path)


def test_json_reader_raises_error_for_invalid_extension():
    file_path = Path("data/raw/ventas_prueba.txt")

    reader = JSONReader()

    with pytest.raises(ValueError):
        reader.read(file_path)
