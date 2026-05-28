from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.modules.reminders.models import DoseLog, Reminder
from app.modules.reminders.schemas import ReminderCreate, ReminderUpdate


def list_reminders(db: Session) -> list[Reminder]:
    statement = select(Reminder).options(joinedload(Reminder.medication)).order_by(Reminder.id)
    return list(db.scalars(statement).all())


def list_today_reminders(db: Session) -> list[Reminder]:
    statement = (
        select(Reminder)
        .options(joinedload(Reminder.medication))
        .where(Reminder.is_active.is_(True))
        .order_by(Reminder.time_of_day)
    )
    return list(db.scalars(statement).all())


def get_reminder(db: Session, reminder_id: int) -> Reminder | None:
    statement = select(Reminder).options(joinedload(Reminder.medication)).where(Reminder.id == reminder_id)
    return db.scalars(statement).first()


def create_reminder(db: Session, reminder_in: ReminderCreate) -> Reminder:
    reminder = Reminder(**reminder_in.model_dump())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return get_reminder(db, reminder.id) or reminder


def update_reminder(db: Session, reminder: Reminder, reminder_in: ReminderUpdate) -> Reminder:
    for field, value in reminder_in.model_dump(exclude_unset=True).items():
        setattr(reminder, field, value)
    db.commit()
    db.refresh(reminder)
    return get_reminder(db, reminder.id) or reminder


def delete_reminder(db: Session, reminder: Reminder) -> None:
    db.delete(reminder)
    db.commit()


def create_taken_log(db: Session, reminder: Reminder) -> DoseLog:
    dose_log = DoseLog(reminder_id=reminder.id, status="taken")
    db.add(dose_log)
    db.commit()
    db.refresh(dose_log)
    return dose_log
