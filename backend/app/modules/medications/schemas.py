from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MedicationBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    dose_label: str = Field(min_length=1, max_length=120)

    @field_validator("name", "dose_label")
    @classmethod
    def strip_and_reject_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned


class MedicationCreate(MedicationBase):
    pass


class MedicationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    dose_label: str | None = Field(default=None, min_length=1, max_length=120)

    @field_validator("name", "dose_label")
    @classmethod
    def strip_optional_and_reject_blank(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned


class MedicationRead(MedicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
