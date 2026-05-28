from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.reminders import service
from app.modules.reminders.schemas import DoseLogRead, ReminderCreate, ReminderRead, ReminderUpdate


router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.post("", response_model=ReminderRead, status_code=status.HTTP_201_CREATED)
def create_reminder(reminder_in: ReminderCreate, db: Session = Depends(get_db)):
    return service.create_reminder(db, reminder_in)


@router.get("", response_model=list[ReminderRead])
def list_reminders(db: Session = Depends(get_db)):
    return service.list_reminders(db)


@router.get("/today", response_model=list[ReminderRead])
def list_today_reminders(db: Session = Depends(get_db)):
    return service.list_today_reminders(db)


@router.get("/{reminder_id}", response_model=ReminderRead)
def get_reminder(reminder_id: int, db: Session = Depends(get_db)):
    return service.get_reminder_or_404(db, reminder_id)


@router.patch("/{reminder_id}", response_model=ReminderRead)
def update_reminder(
    reminder_id: int,
    reminder_in: ReminderUpdate,
    db: Session = Depends(get_db),
):
    return service.update_reminder(db, reminder_id, reminder_in)


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    service.delete_reminder(db, reminder_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{reminder_id}/taken", response_model=DoseLogRead, status_code=status.HTTP_201_CREATED)
def mark_reminder_taken(reminder_id: int, db: Session = Depends(get_db)):
    return service.mark_taken(db, reminder_id)
