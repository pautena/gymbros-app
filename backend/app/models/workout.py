import uuid
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Workout(SQLModel, table=True):
  id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  name: Optional[str]
  created_at: datetime = Field(default_factory=datetime.now)
  updated_at: Optional[datetime] = Field(
    default_factory=datetime.now,
    sa_column_kwargs={"onupdate": datetime.now},
  )
 