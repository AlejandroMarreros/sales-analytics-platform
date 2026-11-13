from pathlib import Path

import pytest

from ml_platform.ingestion.reader_factory import ReaderFactory


def test_reader_factory_rejects_large_file(tmp_path: Path) -> None:
    path = tmp_path / "large.csv"
    path.write_bytes(b"x" * (1024 * 1024))  # 1 MB

    # El límite por defecto es 500 MB; aquí forzamos un límite bajo
    # monkeypatchando la constante en file_limits
    from ml_platform.ingestion import file_limits

    original = file_limits.MAX_FILE_SIZE_MB
    file_limits.MAX_FILE_SIZE_MB = 0.5
    try:
        with pytest.raises(ValueError, match="demasiado grande"):
            ReaderFactory.create(path)
    finally:
        file_limits.MAX_FILE_SIZE_MB = original


def test_reader_factory_accepts_small_file(tmp_path: Path) -> None:
    path = tmp_path / "small.csv"
    path.write_text("ventas\n100\n")

    reader = ReaderFactory.create(path)

    assert reader is not None


def test_reader_factory_raises_when_file_missing(tmp_path: Path) -> None:
    path = tmp_path / "no_existe.csv"

    with pytest.raises(FileNotFoundError):
        ReaderFactory.create(path)
