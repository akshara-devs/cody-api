from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import date, datetime
from uuid import UUID

class ProjectCU(BaseModel):
  user_id: UUID
  name: str = Field(
    ...,
    max_length= 64
  )
  description: str = Field(
    ...,
    max_length= 1000
  )
  due_date: date 
  min_session_time: int = Field(
    ...,
    ge=900
  )
  @field_validator("name", "description")
  @classmethod
  def validate_text_fields(cls, value: str) -> str:
    value = value.strip()

    if(not value):
        raise ValueError("Text fields cannot be empty!")
    return value
  
  @field_validator("user_id")
  @classmethod
  def validate_user_id(cls, value: UUID) -> UUID:
     value = value.strip()

     if(not value):
        raise ValueError("User ID cannot be empty!")
     return value
  
  @field_validator("due_date")
  @classmethod
  def validate_due_date(cls, value: date) -> date:
     if(value < date.today()):
        raise ValueError("Cannot have a deadline in the past!")
     if(not value):
        raise ValueError("Deadline cannot be empty!")
     return value
  
  @field_validator("min_session_time")
  @classmethod
  def validate_min_session_time(cls, value: int)->int:
     value = value.strip()

     if(not value):
        raise ValueError("Minimum session time cannot be empty!")
     return value
     
class ProjectResponse(BaseModel):
   id: int
   user_id: UUID
   name: str
   description: str
   due_date: date
   min_session_time: int
   created_at: datetime
   modified_at: datetime

model_config = ConfigDict(from_attributes=True)