from ml_platform.preprocessing.normalization.result import NormalizationResult


def test_normalization_result_is_valid_without_type_errors():
    result = NormalizationResult(dataframe=None, renamed=(), type_errors=(), skipped=())

    assert result.valid is True


def test_normalization_result_is_invalid_with_type_errors():
    result = NormalizationResult(
        dataframe=None,
        renamed=(),
        type_errors=("ventas contiene valores no numéricos",),
        skipped=(),
    )

    assert result.valid is False


def test_normalization_result_does_not_expose_mutable_collections():
    result = NormalizationResult(
        dataframe=None,
        renamed=(("sales", "ventas"),),
        type_errors=(),
        skipped=(),
    )

    assert isinstance(result.renamed, tuple)
    assert isinstance(result.type_errors, tuple)
    assert isinstance(result.skipped, tuple)
