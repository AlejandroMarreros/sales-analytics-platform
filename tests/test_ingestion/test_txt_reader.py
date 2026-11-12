from pathlib import Path

import pandas as pd
import pytest

from ml_platform.ingestion.txt_reader import TXTReader


def test_txt_reader_reads_valid_txt():
    file_path = Path("data/raw/ventas_prueba.txt")

    reader = TXTReader()
    result = reader.read(file_path)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert list(result.columns) == ["text"]
    assert result.iloc[0]["text"] == "esto es un archivo de texto"


def test_txt_reader_raises_error_when_file_does_not_exist():
    file_path = Path("data/raw/archivo_inexistente.txt")

    reader = TXTReader()

    with pytest.raises(FileNotFoundError):
        reader.read(file_path)


def test_txt_reader_raises_error_for_invalid_extension():
    file_path = Path("data/raw/ventas_prueba.csv")

    reader = TXTReader()

    with pytest.raises(ValueError):
        reader.read(file_path)
