from app.models.workout import Workout, WorkoutCreate, WorkoutsPublic
from fastapi import APIRouter
from typing import Any
from app.api.deps import (
    SessionDep, CurrentUser
)
from sqlmodel import func, select

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.get("/", response_model=WorkoutsPublic)
async def list_workouts(*, session: SessionDep, current_user: CurrentUser, skip:int=0,limit:int=100) -> Any:
    count_statement = (
        select(func.count())
        .select_from(Workout)
        .where(Workout.owner_id == current_user.id)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Workout)
        .where(Workout.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    workouts = session.exec(statement).all()
    return WorkoutsPublic(data=workouts, count=count)

@router.post("/", response_model=Workout)
async def create_workout(*, session: SessionDep, current_user: CurrentUser, workout_in: WorkoutCreate) -> Any:
    workout = Workout.model_validate(workout_in, update={"owner_id": current_user.id})
    session.add(workout)
    session.commit()
    session.refresh(workout)
    return workout