"""
This module provides helper functions for validating API parameters

"""

from fastapi import HTTPException
from typing import List

def validate_include_param(include: List[str], allowed_includes: List[str]):
    """
    Validates that each item in `include` is in the allowed fields list.

    Parameters:
        include (List[str]): List of fields to validate.
        allowed_includes (List[str]): List of allowed fields.

    Raises:
        HTTPException: If any field in `include` is not allowed.
    """
    invalid_fields = set(include) - set(allowed_includes)
    if invalid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid fields in include parameter: {invalid_fields}")
