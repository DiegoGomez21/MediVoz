# Backend CRUD de Alarmas Sprint 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the FastAPI backend for MediVoz Sprint 1: medications CRUD, basic reminders/alarms CRUD, today's reminders, and dose confirmation.

**Architecture:** Keep the existing FastAPI app modular. Add SQLAlchemy with SQLite persistence, a small database module, and focused medication/reminder modules with `models`, `schemas`, `repository`, `service`, and `router` files.

**Tech Stack:** Python, FastAPI, SQLAlchemy 2.x, SQLite, Pydantic v2, pytest, FastAPI TestClient.

---

## File Structure

- Modify: `backend/requirements.txt` — add SQLAlchemy runtime dependency.
- Create: `backend/app/database.py` — SQLAlchemy engine/session/base configuration.
- Modify: `backend/app/main.py` — app factory, table creation on startup, router registration.
- Create: `backend/app/models.py` — import all ORM models before table creation.
- Create: `backend/app/modules/medications/__init__.py` — medication module marker.
- Create: `backend/app/modules/medications/models.py` — `Medication` ORM model.
- Create: `backend/app/modules/medications/schemas.py` — medication request/response schemas.
- Create: `backend/app/modules/medications/repository.py` — medication persistence operations.
- Create: `backend/app/modules/medications/service.py` — medication business errors and orchestration.
- Create: `backend/app/modules/medications/router.py` — medication HTTP endpoints.
- Create: `backend/app/modules/reminders/__init__.py` — reminder module marker.
- Create: `backend/app/modules/reminders/models.py` — `Reminder` and `DoseLog` ORM models.
- Create: `backend/app/modules/reminders/schemas.py` — reminder and dose log schemas.
- Create: `backend/app/modules/reminders/repository.py` — reminder and dose log persistence operations.
- Create: `backend/app/modules/reminders/service.py` — reminder business errors and orchestration.
- Create: `backend/app/modules/reminders/router.py` — reminder HTTP endpoints.
- Create: `backend/tests/conftest.py` — temporary SQLite database and test client fixture.
- Modify: `backend/tests/test_health.py` — use the shared test client fixture.
- Create: `backend/tests/test_medications.py` — medication CRUD behavior.
- Create: `backend/tests/test_reminders.py` — reminder CRUD, validation, today query, and taken log behavior.
- Modify: `backend/README.md` — document SQLAlchemy dependency and new endpoint groups.

No git commit step is included because the repository instructions require an explicit user request before committing.

## Task 1: SQLAlchemy Foundation and Test Fixture

**Files:**
- Modify: `backend/requirements.txt`
- Create: `backend/app/database.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/conftest.py`
- Modify: `backend/tests/test_health.py`

- [ ] **Step 1: Add SQLAlchemy dependency**

Update `backend/requirements.txt` to:

```text
fastapi==0.115.6
uvicorn[standard]==0.34.0
SQLAlchemy==2.0.36
pydantic==2.13.4
```

- [ ] **Step 2: Create database module**

Create `backend/app/database.py`:

```python
import os
from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DEFAULT_DATABASE_URL = "sqlite:///./medivoz.db"


class Base(DeclarativeBase):
    pass


def _create_engine(database_url: str) -> Engine:
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    db_engine = create_engine(database_url, connect_args=connect_args)

    if database_url.startswith("sqlite"):

        @event.listens_for(db_engine, "connect")
        def _enable_sqlite_foreign_keys(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return db_engine


DATABASE_URL = os.getenv("MEDIVOZ_DATABASE_URL", DEFAULT_DATABASE_URL)
engine = _create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def configure_database(database_url: str) -> None:
    global DATABASE_URL, engine, SessionLocal

    DATABASE_URL = database_url
    engine = _create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 3: Refactor app creation**

Modify `backend/app/main.py` to:

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import database, models
from app.modules.health.router import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    database.Base.metadata.create_all(bind=database.engine)
    yield


async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": jsonable_encoder(exc.errors())},
    )


def create_app() -> FastAPI:
    app = FastAPI(title="MediVoz API", lifespan=lifespan)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    return app


app = create_app()
```

- [ ] **Step 4: Create model registry file**

Create `backend/app/models.py`:

```python
__all__: list[str] = []
```

- [ ] **Step 5: Add isolated test client fixture**

Create `backend/tests/conftest.py`:

```python
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import create_app


@pytest.fixture()
def client(tmp_path) -> Generator[TestClient, None, None]:
    database_path = tmp_path / "test.db"
    database.configure_database(f"sqlite:///{database_path}")

    app = create_app()

    with TestClient(app) as test_client:
        yield test_client

    database.Base.metadata.drop_all(bind=database.engine)
```

- [ ] **Step 6: Update health test to use fixture**

Modify `backend/tests/test_health.py` to:

```python
from fastapi.testclient import TestClient


def test_health_endpoint_reports_service_status(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "medivoz-api"}
```

- [ ] **Step 7: Run health test**

Run: `pytest tests/test_health.py -v`

Expected: the health test passes and no medication/reminder endpoints exist yet.

## Task 2: Medication CRUD

**Files:**
- Create: `backend/app/modules/medications/__init__.py`
- Create: `backend/app/modules/medications/models.py`
- Create: `backend/app/modules/medications/schemas.py`
- Create: `backend/app/modules/medications/repository.py`
- Create: `backend/app/modules/medications/service.py`
- Create: `backend/app/modules/medications/router.py`
- Modify: `backend/app/models.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/test_medications.py`

- [ ] **Step 1: Write medication CRUD tests**

Create `backend/tests/test_medications.py`:

```python
from fastapi.testclient import TestClient


def test_create_and_list_medications(client: TestClient):
    create_response = client.post(
        "/medications",
        json={"name": "Metformina", "dose_label": "500 mg"},
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] == 1
    assert created["name"] == "Metformina"
    assert created["dose_label"] == "500 mg"
    assert "created_at" in created
    assert "updated_at" in created

    list_response = client.get("/medications")

    assert list_response.status_code == 200
    assert list_response.json() == [created]


def test_get_patch_and_delete_medication(client: TestClient):
    medication = client.post(
        "/medications",
        json={"name": "Losartan", "dose_label": "50 mg"},
    ).json()

    get_response = client.get(f"/medications/{medication['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Losartan"

    patch_response = client.patch(
        f"/medications/{medication['id']}",
        json={"dose_label": "100 mg"},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["dose_label"] == "100 mg"

    delete_response = client.delete(f"/medications/{medication['id']}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/medications/{medication['id']}")
    assert missing_response.status_code == 404


def test_medication_rejects_blank_fields(client: TestClient):
    response = client.post(
        "/medications",
        json={"name": "   ", "dose_label": "500 mg"},
    )

    assert response.status_code == 400
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert detail[0]["loc"] == ["body", "name"]
```

- [ ] **Step 2: Run medication tests to verify failure**

Run: `pytest tests/test_medications.py -v`

Expected: tests fail with `404 Not Found` for `/medications` because the module is not implemented.

- [ ] **Step 3: Create medication ORM model**

Create `backend/app/modules/medications/__init__.py`:

```python
```

Create `backend/app/modules/medications/models.py`:

```python
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Medication(Base):
    __tablename__ = "medications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    dose_label: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    reminders = relationship("Reminder", back_populates="medication", cascade="all, delete-orphan")
```

- [ ] **Step 4: Create medication schemas**

Create `backend/app/modules/medications/schemas.py`:

```python
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
```

- [ ] **Step 5: Create medication repository and service**

Create `backend/app/modules/medications/repository.py`:

```python
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
```

Create `backend/app/modules/medications/service.py`:

```python
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
```

- [ ] **Step 6: Create medication router**

Create `backend/app/modules/medications/router.py`:

```python
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
```

- [ ] **Step 7: Register medication model and router**

Modify `backend/app/models.py` to:

```python
from app.modules.medications.models import Medication


__all__ = ["Medication"]
```

Modify `backend/app/main.py` to:

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import database, models
from app.modules.health.router import router as health_router
from app.modules.medications.router import router as medications_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    database.Base.metadata.create_all(bind=database.engine)
    yield


async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": jsonable_encoder(exc.errors())},
    )


def create_app() -> FastAPI:
    app = FastAPI(title="MediVoz API", lifespan=lifespan)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(medications_router)
    return app


app = create_app()
```

- [ ] **Step 8: Run medication tests**

Run: `pytest tests/test_health.py tests/test_medications.py -v`

Expected: all health and medication tests pass.

## Task 3: Reminder CRUD and Dose Confirmation

**Files:**
- Create: `backend/app/modules/reminders/__init__.py`
- Create: `backend/app/modules/reminders/models.py`
- Create: `backend/app/modules/reminders/schemas.py`
- Create: `backend/app/modules/reminders/repository.py`
- Create: `backend/app/modules/reminders/service.py`
- Create: `backend/app/modules/reminders/router.py`
- Modify: `backend/app/models.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/test_reminders.py`

- [ ] **Step 1: Write reminder tests**

Create `backend/tests/test_reminders.py`:

```python
from fastapi.testclient import TestClient


def create_medication(client: TestClient, name: str = "Metformina") -> dict:
    return client.post("/medications", json={"name": name, "dose_label": "500 mg"}).json()


def test_create_and_list_reminders(client: TestClient):
    medication = create_medication(client)

    create_response = client.post(
        "/reminders",
        json={"medication_id": medication["id"], "time_of_day": "08:30", "is_active": True},
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] == 1
    assert created["medication_id"] == medication["id"]
    assert created["time_of_day"] == "08:30"
    assert created["is_active"] is True
    assert created["medication"]["name"] == "Metformina"

    list_response = client.get("/reminders")

    assert list_response.status_code == 200
    assert list_response.json() == [created]


def test_get_patch_and_delete_reminder(client: TestClient):
    medication = create_medication(client, name="Losartan")
    reminder = client.post(
        "/reminders",
        json={"medication_id": medication["id"], "time_of_day": "07:00"},
    ).json()

    get_response = client.get(f"/reminders/{reminder['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["time_of_day"] == "07:00"

    patch_response = client.patch(
        f"/reminders/{reminder['id']}",
        json={"time_of_day": "09:15", "is_active": False},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["time_of_day"] == "09:15"
    assert patch_response.json()["is_active"] is False

    delete_response = client.delete(f"/reminders/{reminder['id']}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/reminders/{reminder['id']}")
    assert missing_response.status_code == 404


def test_reminder_requires_existing_medication(client: TestClient):
    response = client.post(
        "/reminders",
        json={"medication_id": 999, "time_of_day": "08:00"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Medication does not exist"


def test_reminder_rejects_invalid_time(client: TestClient):
    medication = create_medication(client)

    response = client.post(
        "/reminders",
        json={"medication_id": medication["id"], "time_of_day": "25:90"},
    )

    assert response.status_code == 400
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert detail[0]["loc"] == ["body", "time_of_day"]


def test_today_reminders_returns_active_reminders_ordered_by_time(client: TestClient):
    medication = create_medication(client)

    client.post("/reminders", json={"medication_id": medication["id"], "time_of_day": "18:00"})
    client.post("/reminders", json={"medication_id": medication["id"], "time_of_day": "08:00"})
    client.post(
        "/reminders",
        json={"medication_id": medication["id"], "time_of_day": "06:00", "is_active": False},
    )

    response = client.get("/reminders/today")

    assert response.status_code == 200
    assert [item["time_of_day"] for item in response.json()] == ["08:00", "18:00"]


def test_mark_reminder_taken_creates_dose_log(client: TestClient):
    medication = create_medication(client)
    reminder = client.post(
        "/reminders",
        json={"medication_id": medication["id"], "time_of_day": "08:00"},
    ).json()

    response = client.post(f"/reminders/{reminder['id']}/taken")

    assert response.status_code == 201
    dose_log = response.json()
    assert dose_log["reminder_id"] == reminder["id"]
    assert dose_log["status"] == "taken"
    assert "taken_at" in dose_log
    assert "created_at" in dose_log
```

- [ ] **Step 2: Run reminder tests to verify failure**

Run: `pytest tests/test_reminders.py -v`

Expected: tests fail with `404 Not Found` for `/reminders` because the module is not implemented.

- [ ] **Step 3: Create reminder ORM models**

Create `backend/app/modules/reminders/__init__.py`:

```python
```

Create `backend/app/modules/reminders/models.py`:

```python
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    medication_id: Mapped[int] = mapped_column(ForeignKey("medications.id", ondelete="CASCADE"), nullable=False, index=True)
    time_of_day: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    medication = relationship("Medication", back_populates="reminders")
    dose_logs = relationship("DoseLog", back_populates="reminder", cascade="all, delete-orphan")


class DoseLog(Base):
    __tablename__ = "dose_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reminder_id: Mapped[int] = mapped_column(ForeignKey("reminders.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="taken", nullable=False)
    taken_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    reminder = relationship("Reminder", back_populates="dose_logs")
```

- [ ] **Step 4: Create reminder schemas**

Create `backend/app/modules/reminders/schemas.py`:

```python
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
```

- [ ] **Step 5: Create reminder repository and service**

Create `backend/app/modules/reminders/repository.py`:

```python
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
```

Create `backend/app/modules/reminders/service.py`:

```python
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
```

- [ ] **Step 6: Create reminder router**

Create `backend/app/modules/reminders/router.py`:

```python
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
```

- [ ] **Step 7: Register reminder models and router**

Modify `backend/app/models.py` to:

```python
from app.modules.medications.models import Medication
from app.modules.reminders.models import DoseLog, Reminder


__all__ = ["Medication", "Reminder", "DoseLog"]
```

Modify `backend/app/main.py` to:

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import database, models
from app.modules.health.router import router as health_router
from app.modules.medications.router import router as medications_router
from app.modules.reminders.router import router as reminders_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    database.Base.metadata.create_all(bind=database.engine)
    yield


async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": jsonable_encoder(exc.errors())},
    )


def create_app() -> FastAPI:
    app = FastAPI(title="MediVoz API", lifespan=lifespan)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(medications_router)
    app.include_router(reminders_router)
    return app


app = create_app()
```

- [ ] **Step 8: Run reminder tests**

Run: `pytest tests/test_health.py tests/test_medications.py tests/test_reminders.py -v`

Expected: all health, medication, and reminder tests pass.

## Task 4: Backend Documentation and Full Verification

**Files:**
- Modify: `backend/README.md`

- [ ] **Step 1: Update backend README**

Modify `backend/README.md` to include these endpoint groups after the health endpoint section:

```markdown
## Endpoints Sprint 1

Medicamentos:

- `POST /medications`
- `GET /medications`
- `GET /medications/{medication_id}`
- `PATCH /medications/{medication_id}`
- `DELETE /medications/{medication_id}`

Recordatorios/alarmas basicas:

- `POST /reminders`
- `GET /reminders`
- `GET /reminders/today`
- `GET /reminders/{reminder_id}`
- `PATCH /reminders/{reminder_id}`
- `DELETE /reminders/{reminder_id}`
- `POST /reminders/{reminder_id}/taken`

La persistencia usa SQLite con SQLAlchemy. Por defecto la API crea `medivoz.db` en el directorio desde el que se ejecuta `uvicorn`.
```

- [ ] **Step 2: Run full test suite**

Run: `pytest -v`

Expected: all tests pass.

- [ ] **Step 3: Check working tree**

Run: `git status --short`

Expected: changes are visible and uncommitted. Do not create a commit unless the user explicitly asks for one.

## Self-Review

- Spec coverage: medications CRUD, reminders CRUD, today's reminders, dose confirmation, SQLAlchemy persistence, and pytest coverage all have tasks.
- Scope check: authentication, patients, inventory, voice, advanced alarm parameters, and reports are excluded.
- Type consistency: paths, schema names, router prefixes, and model field names match across tasks.
- Verification: the final task runs the full `pytest -v` suite.
