from pathlib import Path

import pandas as pd

from .base_reader import BaseReader


class ExcelReader(BaseReader):
    """Lector de archivos Excel."""

    def read(self, file_path: Path) -> pd.DataFrame:
        """
        Lee un archivo Excel y devuelve un DataFrame.

        Args:
            file_path: Ruta del archivo Excel.

        Returns:
            DataFrame con los datos.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si el archivo no tiene una extensión Excel válida.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

        if file_path.suffix.lower() not in {".xlsx", ".xls"}:
            raise ValueError(f"El archivo no es Excel: {file_path}")

        return pd.read_excel(file_path)
