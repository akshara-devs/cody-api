import secrets
from typing import Annotated

from fastapi import Header, HTTPException, status
from core.config import settings

def verify_internal_api_key(
  x_internal_api_key: Annotated[str, Header(...)]
) -> None:
  expected = settings.internal_api_key
  if not expected:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Internal API key is missing.",
    )
  if x_internal_api_key is None or not secrets.compare_digest(x_internal_api_key, expected):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid or missing API key.",
    )
  return None
