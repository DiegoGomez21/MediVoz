from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.medications.models import Medication
from app.modules.medications.schemas import MedicationCreate, MedicationUpdate


def list_medications(db: Session) -> list[Medication]:
    return list(db.scalars(select(Medication).order_by(Medication.id)).all())


def get_medication(db: Session, medication_id: int) -> Medication | None:
    return db.get(Medication, medication_id)


def create_medication(db: Session, medication_in: MedicationCreate) -> Medication:
    medication = Medication(**medication_in.model_dump())
    db.add(medication)
    db.commit()
    db.refresh(medication)
    return medication


def update_medication(db: Session, medication: Medication, medication_in: MedicationUpdate) -> Medication:
    for field, value in medication_in.model_dump(exclude_unset=True).items():
        setattr(medication, field, value)
    db.commit()
    db.refresh(medication)
    return medication


def delete_medication(db: Session, medication: Medication) -> None:
    db.delete(medication)
    db.commit()
