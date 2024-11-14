"""
Tests for the validation utility functions.
"""

import pytest
from fastapi import HTTPException
from src.utils.validators import validate_include_param
from src.utils.constants import ALLOWED_INCLUDES_POSTS, ALLOWED_INCLUDES_USERS

def test_validate_include_param_valid_posts():
    """Test `validate_include_param` with valid fields for posts, expecting no exception."""
    include = list(ALLOWED_INCLUDES_POSTS)
    try:
        validate_include_param(include, ALLOWED_INCLUDES_POSTS)
    except HTTPException:
        pytest.fail("validate_include_param raised HTTPException unexpectedly!")

def test_validate_include_param_valid_users():
    """Test `validate_include_param` with valid fields for users, expecting no exception."""
    include = list(ALLOWED_INCLUDES_USERS)
    try:
        validate_include_param(include, ALLOWED_INCLUDES_USERS)
    except HTTPException:
        pytest.fail("validate_include_param raised HTTPException unexpectedly!")

def test_validate_include_param_invalid_posts():
    """Test `validate_include_param` with an invalid field for posts, expecting a 400 error."""
    include = ["invalid_field"]
    with pytest.raises(HTTPException) as exc_info:
        validate_include_param(include, ALLOWED_INCLUDES_POSTS)
    assert exc_info.value.status_code == 400
    assert "Invalid fields in include parameter" in exc_info.value.detail

def test_validate_include_param_invalid_users():
    """Test `validate_include_param` with an invalid field for users, expecting a 400 error."""
    include = ["invalid_field"]
    with pytest.raises(HTTPException) as exc_info:
        validate_include_param(include, ALLOWED_INCLUDES_USERS)
    assert exc_info.value.status_code == 400
    assert "Invalid fields in include parameter" in exc_info.value.detail
