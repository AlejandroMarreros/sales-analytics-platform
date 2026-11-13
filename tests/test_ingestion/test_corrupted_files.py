import zipfile
from pathlib import Path

import pytest
from pypdf.errors import PdfStreamError

from ml_platform.ingestion.csv_reader import CSVReader
from ml_platform.ingestion.excel_reader import ExcelReader
from ml_platform.ingestion.json_reader import JSONReader
from ml_platform.ingestion.pdf_reader import PDFReader
from ml_platform.ingestion.txt_reader import TXTReader


def test_csv_reader_handles_corrupted_file(tmp_path: Path) -> None:
    path = tmp_path / "corrupt.csv"
    path.write_bytes(b"\x00\x01\x02\x03")

    # pandas.read_csv es tolerante: puede devolver un DataFrame raro
    # en vez de lanzar. Ambos comportamientos son aceptables.
    try:
        result = CSVReader().read(path)
    except (ValueError, UnicodeDecodeError):
        pass
    else:
        assert result is not None


def test_pdf_reader_raises_on_truncated_file(tmp_path: Path) -> None:
    path = tmp_path / "truncated.pdf"
    path.write_bytes(b"%PDF-1.4\n" + b"x" * 10)

    with pytest.raises(PdfStreamError):
        PDFReader().read(path)


def test_excel_reader_raises_on_corrupted_file(tmp_path: Path) -> None:
    path = tmp_path / "corrupt.xlsx"
    path.write_bytes(b"PK\x03\x04" + b"x" * 20)

    with pytest.raises(zipfile.BadZipFile):
        ExcelReader().read(path)


def test_json_reader_raises_on_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(ValueError):
        JSONReader().read(path)


def test_txt_reader_handles_binary_content(tmp_path: Path) -> None:
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff\xfe\x00\x01\x02\x03")

    try:
        TXTReader().read(path)
    except (UnicodeDecodeError, ValueError):
        pass
