from ml_platform.preprocessing.validation.result import ValidationResult


def test_validation_result_is_valid_when_no_errors_or_warnings():
    result = ValidationResult()

    assert result.valid is True
    assert result.errors == ()
    assert result.warnings == ()


def test_validation_result_is_invalid_when_has_errors():
    result = ValidationResult(errors=("DataFrame vacío",))

    assert result.valid is False
    assert result.errors == ("DataFrame vacío",)
    assert result.warnings == ()


def test_validation_result_remains_valid_with_warnings():
    result = ValidationResult(warnings=("Existen valores faltantes",))

    assert result.valid is True
    assert result.errors == ()
    assert result.warnings == ("Existen valores faltantes",)


def test_validation_result_accepts_multiple_errors_and_warnings():
    result = ValidationResult(
        errors=("Columnas duplicadas", "Tipo inválido"),
        warnings=("Valores faltantes", "Fecha sospechosa"),
    )

    assert result.valid is False
    assert result.errors == ("Columnas duplicadas", "Tipo inválido")
    assert result.warnings == ("Valores faltantes", "Fecha sospechosa")


def test_validation_result_does_not_expose_mutable_collections():
    errors = ["Error de prueba"]
    warnings = ["Advertencia de prueba"]

    result = ValidationResult(errors=errors, warnings=warnings)

    errors.append("Otro error")
    warnings.append("Otra advertencia")

    assert result.errors == ("Error de prueba",)
    assert result.warnings == ("Advertencia de prueba",)
