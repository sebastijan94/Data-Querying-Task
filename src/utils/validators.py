from fastapi import HTTPException, status
from typing import List
from src.utils.constants import ALLOWED_INCLUDES

def validate_include_param(include: List[str]):
    invalid_fields = [field for field in include if field not in ALLOWED_INCLUDES]
    if invalid_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid fields in include parameter: {', '.join(invalid_fields)}. "
                   f"Allowed values are: {', '.join(ALLOWED_INCLUDES)}."
        )
