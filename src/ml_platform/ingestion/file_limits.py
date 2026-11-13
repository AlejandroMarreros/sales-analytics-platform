from pathlib import Path

MAX_FILE_SIZE_MB = 500


def check_file_size(path: Path, max_mb: int | None = None) -> None:
    """Verifica que el archivo no exceda el tamaño máximo permitido.

    Lanza ValueError si supera el límite. El objetivo es evitar DoS
    accidental (archivos gigantes que cuelguen la máquina), no imponer
    límites arbitrarios a usuarios legítimos.

    Args:
        path: Ruta del archivo.
        max_mb: Tamaño máximo en megabytes. Si es None, usa
            MAX_FILE_SIZE_MB (500 MB por defecto).

    Raises:
        ValueError: Si el archivo existe y su tamaño supera el límite.
        FileNotFoundError: Si el archivo no existe.
    """
    if max_mb is None:
        max_mb = MAX_FILE_SIZE_MB

    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")

    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > max_mb:
        raise ValueError(
            f"Archivo demasiado grande: {size_mb:.1f} MB "
            f"(máximo permitido: {max_mb} MB)"
        )
