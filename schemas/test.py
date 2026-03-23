from pydantic import BaseModel, ConfigDict, Field, field_validator


class TestCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Name for the test record.",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized_value = value.strip()
        if not normalized_value:
            raise ValueError("Name must not be blank.")
        return normalized_value


class TestResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
