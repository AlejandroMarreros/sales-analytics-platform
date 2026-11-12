from pathlib import Path

import pandas as pd

from .base_reader import BaseReader


class TXTReader(BaseReader):
    """Lector de archivos de texto."""

    def read(self, file_path: Path) -> pd.DataFrame:
        """
        Lee un archivo TXT y devuelve su contenido como DataFrame.

        Args:
            file_path: Ruta del archivo TXT.

        Returns:
            DataFrame con una fila por línea.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si el archivo no es TXT.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

        if file_path.suffix.lower() != ".txt":
            raise ValueError(f"El archivo no es TXT: {file_path}")

        with file_path.open("r", encoding="utf-8") as file:
            lines = [line.rstrip("\n") for line in file]

        return pd.DataFrame({"text": lines})
