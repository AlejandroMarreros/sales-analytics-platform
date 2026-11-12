from pathlib import Path

import pandas as pd

from .base_reader import BaseReader


class CSVReader(BaseReader):
    """Lector de archivos CSV."""

    def read(self, file_path: Path) -> pd.DataFrame:
        """
        Lee un archivo CSV y devuelve un DataFrame.

        Args:
            file_path: Ruta del archivo CSV.

        Returns:
            DataFrame con los datos del archivo.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si el archivo no tiene extensión CSV.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

        if file_path.suffix.lower() != ".csv":
            raise ValueError(f"El archivo no es CSV: {file_path}")

        return pd.read_csv(file_path)
