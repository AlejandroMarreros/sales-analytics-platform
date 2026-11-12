from pathlib import Path

import pandas as pd

from .base_reader import BaseReader


class JSONReader(BaseReader):
    """Lector de archivos JSON."""

    def read(self, file_path: Path) -> pd.DataFrame:
        """
        Lee un archivo JSON y devuelve un DataFrame.

        Args:
            file_path: Ruta del archivo JSON.

        Returns:
            DataFrame con los datos.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si el archivo no tiene extensión JSON.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

        if file_path.suffix.lower() != ".json":
            raise ValueError(f"El archivo no es JSON: {file_path}")

        return pd.read_json(file_path)
