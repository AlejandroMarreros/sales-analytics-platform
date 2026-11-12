from ml_platform.preprocessing.cleaning.result import CleaningResult


def test_cleaning_result_is_valid_without_rows_dropped():
    result = CleaningResult(dataframe=None, rows_dropped=0)

    assert result.valid is True


def test_cleaning_result_is_always_valid_even_with_drops():
    result = CleaningResult(
        dataframe=None,
        rows_dropped=5,
        dropped_reasons=("5 filas duplicadas",),
    )

    assert result.valid is True


def test_cleaning_result_does_not_expose_mutable_collections():
    result = CleaningResult(
        dataframe=None,
        rows_dropped=1,
        dropped_reasons=("1 fila duplicada",),
    )

    assert isinstance(result.dropped_reasons, tuple)
