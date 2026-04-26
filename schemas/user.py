from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator

class UserCreate(BaseModel):
  discord_user_id: str = Field(
    ...,
    min_length=17,
    max_length=21
  )

  @field_validator("discord_user_id")
  @classmethod
  def validate_discord_user_id(cls, value: str) -> str:
    normalized_value = value.strip()
    if not normalized_value:
      raise ValueError("Discord user ID must not be blank")
    if not normalized_value.isdigit():
      raise ValueError("Discord user ID must contain only digits.")
    return normalized_value

class UserDelete(BaseModel):
  discord_user_id: str = Field(
    ...,
    min_length=17,
    max_length=21
  )

  @field_validator("discord_user_id")
  @classmethod
  def validate_discord_user_id(cls, value: str) -> str:
    normalized_value = value.strip()
    if(not normalized_value):
      raise ValueError("Discord user ID must not be blank.")
    if(not normalized_value.isdigit()):
      raise ValueError("Discord user ID must contain only digits.")
    return normalized_value
  
class UserResponse(BaseModel):
  id: UUID
  discord_user_id: str
  created_at: datetime
  modified_at: datetime

  model_config = ConfigDict(from_attributes=True)

