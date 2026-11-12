from pathlib import Path
from typing import ClassVar

from .base_reader import BaseReader
from .csv_reader import CSVReader
from .excel_reader import ExcelReader
from .json_reader import JSONReader
from .pdf_reader import PDFReader
from .txt_reader import TXTReader


class ReaderFactory:
    """Crea el lector adecuado según el tipo de archivo."""

    _READERS: ClassVar[dict[str, type[BaseReader]]] = {
        ".csv": CSVReader,
        ".xlsx": ExcelReader,
        ".xls": ExcelReader,
        ".json": JSONReader,
        ".pdf": PDFReader,
        ".txt": TXTReader,
    }

    @classmethod
    def create(cls, file_path: str | Path) -> BaseReader:
        """
        Crea un lector según la extensión del archivo.

        Args:
            file_path: Ruta del archivo.

        Returns:
            Instancia del lector correspondiente.

        Raises:
            ValueError: Si el formato no está soportado.
        """
        path = Path(file_path)
        extension = path.suffix.lower()

        reader_class = cls._READERS.get(extension)

        if reader_class is None:
            supported = ", ".join(sorted(cls._READERS))

            raise ValueError(
                f"Formato no soportado: '{extension}'. "
                f"Formatos disponibles: {supported}"
            )

        return reader_class()
