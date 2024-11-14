import pytest
from fastapi import HTTPException
from src.utils.validators import validate_include_param
from src.utils.constants import ALLOWED_INCLUDES

def test_validate_include_param_valid():
    include = list(ALLOWED_INCLUDES)
    try:
        validate_include_param(include)
    except HTTPException:
        pytest.fail("validate_include_param raised HTTPException unexpectedly!")

def test_validate_include_param_invalid():
    include = ["invalid_field"]
    with pytest.raises(HTTPException) as exc_info:
        validate_include_param(include)
    assert exc_info.value.status_code == 400
    assert "Invalid fields in include parameter" in exc_info.value.detail
