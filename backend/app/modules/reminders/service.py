from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.medications.repository import get_medication
from app.modules.reminders import repository
from app.modules.reminders.models import DoseLog, Reminder
from app.modules.reminders.schemas import ReminderCreate, ReminderUpdate


def list_reminders(db: Session) -> list[Reminder]:
    return repository.list_reminders(db)


def list_today_reminders(db: Session) -> list[Reminder]:
    return repository.list_today_reminders(db)


def get_reminder_or_404(db: Session, reminder_id: int) -> Reminder:
    reminder = repository.get_reminder(db, reminder_id)
    if reminder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    return reminder


def ensure_medication_exists(db: Session, medication_id: int) -> None:
    if get_medication(db, medication_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Medication does not exist")


def create_reminder(db: Session, reminder_in: ReminderCreate) -> Reminder:
    ensure_medication_exists(db, reminder_in.medication_id)
    return repository.create_reminder(db, reminder_in)


def update_reminder(db: Session, reminder_id: int, reminder_in: ReminderUpdate) -> Reminder:
    reminder = get_reminder_or_404(db, reminder_id)
    if reminder_in.medication_id is not None:
        ensure_medication_exists(db, reminder_in.medication_id)
    return repository.update_reminder(db, reminder, reminder_in)


def delete_reminder(db: Session, reminder_id: int) -> None:
    reminder = get_reminder_or_404(db, reminder_id)
    repository.delete_reminder(db, reminder)


def mark_taken(db: Session, reminder_id: int) -> DoseLog:
    reminder = get_reminder_or_404(db, reminder_id)
    return repository.create_taken_log(db, reminder)
