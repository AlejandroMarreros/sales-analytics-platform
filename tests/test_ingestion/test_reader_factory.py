from pathlib import Path

import pytest

from ml_platform.ingestion.csv_reader import CSVReader
from ml_platform.ingestion.excel_reader import ExcelReader
from ml_platform.ingestion.json_reader import JSONReader
from ml_platform.ingestion.pdf_reader import PDFReader
from ml_platform.ingestion.reader_factory import ReaderFactory
from ml_platform.ingestion.txt_reader import TXTReader


def test_reader_factory_creates_csv_reader():
    reader = ReaderFactory.create(Path("data/raw/ventas_prueba.csv"))
    assert isinstance(reader, CSVReader)


def test_reader_factory_creates_excel_reader():
    reader = ReaderFactory.create(Path("data/raw/ventas_prueba.xlsx"))
    assert isinstance(reader, ExcelReader)


def test_reader_factory_creates_json_reader():
    reader = ReaderFactory.create(Path("data/raw/ventas_prueba.json"))
    assert isinstance(reader, JSONReader)


def test_reader_factory_creates_pdf_reader():
    reader = ReaderFactory.create(Path("data/raw/ventas_prueba.pdf"))
    assert isinstance(reader, PDFReader)


def test_reader_factory_creates_txt_reader():
    reader = ReaderFactory.create(Path("data/raw/ventas_prueba.txt"))
    assert isinstance(reader, TXTReader)


def test_reader_factory_raises_error_for_unsupported_format():
    with pytest.raises(ValueError):
        ReaderFactory.create("data/raw/ventas_prueba.docx")
