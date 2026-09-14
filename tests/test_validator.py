from src import validator
import pytest

# if the input is None
def test_validate_none_input():
    with pytest.raises(ValueError):
        validator.validate(None)

# if the input is empty
def test_validate_empty_bytes():
    with pytest.raises(ValueError):
        validator.validate(b"")

# if the input is too large
def test_validate_large_input():
    with pytest.raises(ValueError):
        validator.validate(b"%PDF-" + b"0" * 11 * 1024 * 1024)

# if the input isn't a pdf
def test_validate_pdf_file_type():
    with pytest.raises(ValueError):
        validator.validate(b"%JPG-")

# if the input is completely valid
def test_validate_valid_input():
    assert validator.validate(b"%PDF-0001111") is None