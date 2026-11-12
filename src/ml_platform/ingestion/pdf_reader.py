from pathlib import Path

import pandas as pd
from pypdf import PdfReader

from .base_reader import BaseReader


class PDFReader(BaseReader):
    """Lector de archivos PDF."""

    def read(self, file_path: Path) -> pd.DataFrame:
        """
        Extrae texto de un PDF y lo devuelve como DataFrame.

        Args:
            file_path: Ruta del archivo PDF.

        Returns:
            DataFrame con una fila por página.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si el archivo no es PDF.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

        if file_path.suffix.lower() != ".pdf":
            raise ValueError(f"El archivo no es PDF: {file_path}")

        reader = PdfReader(file_path)

        rows = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            rows.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

        return pd.DataFrame(rows)
