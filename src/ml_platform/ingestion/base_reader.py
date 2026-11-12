from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseReader(ABC):
    """Clase base para todos los lectores de archivos."""

    @abstractmethod
    def read(self, file_path: Path) -> Any:
        """
        Lee un archivo y devuelve los datos extraídos.

        Args:
            file_path: Ruta del archivo que se desea leer.

        Returns:
            Datos extraídos del archivo.
        """
        raise NotImplementedError
