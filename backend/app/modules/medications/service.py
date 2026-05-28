from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.medications import repository
from app.modules.medications.models import Medication
from app.modules.medications.schemas import MedicationCreate, MedicationUpdate


def list_medications(db: Session) -> list[Medication]:
    return repository.list_medications(db)


def get_medication_or_404(db: Session, medication_id: int) -> Medication:
    medication = repository.get_medication(db, medication_id)
    if medication is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medication not found")
    return medication


def create_medication(db: Session, medication_in: MedicationCreate) -> Medication:
    return repository.create_medication(db, medication_in)


def update_medication(db: Session, medication_id: int, medication_in: MedicationUpdate) -> Medication:
    medication = get_medication_or_404(db, medication_id)
    return repository.update_medication(db, medication, medication_in)


def delete_medication(db: Session, medication_id: int) -> None:
    medication = get_medication_or_404(db, medication_id)
    repository.delete_medication(db, medication)
