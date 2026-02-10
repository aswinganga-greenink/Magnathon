from pydantic import BaseModel, Field
from typing import Literal


class HabitInput(BaseModel):

    """
        Habit score from frontend - 1 to 5
    """

    late_night_usage: float = Field(..., ge=1, le=5)
    app_switching: float = Field(..., ge=1, le=5)
    passive_consumption: float = Field(..., ge=1, le=5)
    sleep_disruption: float = Field(..., ge=1, le=5)
    intentional_breaks: int = Field(..., ge=1, le=5)
    display_name: str | None = None