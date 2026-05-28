from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.medications import service
from app.modules.medications.schemas import MedicationCreate, MedicationRead, MedicationUpdate


router = APIRouter(prefix="/medications", tags=["medications"])


@router.post("", response_model=MedicationRead, status_code=status.HTTP_201_CREATED)
def create_medication(medication_in: MedicationCreate, db: Session = Depends(get_db)):
    return service.create_medication(db, medication_in)


@router.get("", response_model=list[MedicationRead])
def list_medications(db: Session = Depends(get_db)):
    return service.list_medications(db)


@router.get("/{medication_id}", response_model=MedicationRead)
def get_medication(medication_id: int, db: Session = Depends(get_db)):
    return service.get_medication_or_404(db, medication_id)


@router.patch("/{medication_id}", response_model=MedicationRead)
def update_medication(
    medication_id: int,
    medication_in: MedicationUpdate,
    db: Session = Depends(get_db),
):
    return service.update_medication(db, medication_id, medication_in)


@router.delete("/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medication(medication_id: int, db: Session = Depends(get_db)):
    service.delete_medication(db, medication_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
