import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.medications.schemas import MedicationRead


TIME_OF_DAY_PATTERN = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


def validate_time_of_day(value: str) -> str:
    cleaned = value.strip()
    if not TIME_OF_DAY_PATTERN.match(cleaned):
        raise ValueError("time_of_day must use HH:MM 24-hour format")
    return cleaned


class ReminderCreate(BaseModel):
    medication_id: int = Field(gt=0)
    time_of_day: str
    is_active: bool = True

    @field_validator("time_of_day")
    @classmethod
    def validate_create_time_of_day(cls, value: str) -> str:
        return validate_time_of_day(value)


class ReminderUpdate(BaseModel):
    medication_id: int | None = Field(default=None, gt=0)
    time_of_day: str | None = None
    is_active: bool | None = None

    @field_validator("time_of_day")
    @classmethod
    def validate_update_time_of_day(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_time_of_day(value)


class ReminderRead(BaseModel):
    id: int
    medication_id: int
    time_of_day: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    medication: MedicationRead

    model_config = ConfigDict(from_attributes=True)


class DoseLogRead(BaseModel):
    id: int
    reminder_id: int
    status: str
    taken_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
