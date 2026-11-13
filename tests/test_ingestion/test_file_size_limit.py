from pathlib import Path

import pytest

from ml_platform.ingestion.file_limits import check_file_size


def test_check_file_size_accepts_small_file(tmp_path: Path) -> None:
    path = tmp_path / "small.csv"
    path.write_text("ventas\n100\n")

    check_file_size(path)  # no debería lanzar


def test_check_file_size_rejects_large_file(tmp_path: Path) -> None:
    path = tmp_path / "large.csv"
    path.write_bytes(b"x" * (1024 * 1024))  # 1 MB

    with pytest.raises(ValueError, match="demasiado grande"):
        check_file_size(path, max_mb=0.5)


def test_check_file_size_raises_when_file_missing(tmp_path: Path) -> None:
    path = tmp_path / "no_existe.csv"

    with pytest.raises(FileNotFoundError):
        check_file_size(path)
