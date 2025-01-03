import uuid
from app.models.user import User
from sqlmodel import Relationship, SQLModel, Field
from typing import Optional
from datetime import datetime

class WorkoutBase(SQLModel):
    name: Optional[str] = Field(default=None, max_length=255)

class WorkoutCreate(WorkoutBase):
    pass


# Database model, database table inferred from class name
class Workout(WorkoutBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="workouts")

class WorkoutPublic(WorkoutBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

class WorkoutsPublic(SQLModel):
    data: list[WorkoutPublic]
    count: int