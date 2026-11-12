from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    """Resultado inmutable de una validación."""

    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "errors", tuple(self.errors))
        object.__setattr__(self, "warnings", tuple(self.warnings))

    @property
    def valid(self) -> bool:
        """Indica si la validación terminó sin errores."""
        return not self.errors
