from fastapi import HTTPException
from typing import List

def validate_include_param(include: List[str], allowed_includes: List[str]):
    invalid_fields = set(include) - set(allowed_includes)
    if invalid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid fields in include parameter: {invalid_fields}")
