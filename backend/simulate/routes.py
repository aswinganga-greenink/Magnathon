from fastapi import APIRouter, Query
from simulate.validate import HabitInput
from behavioral_engine.engine import run_behavioral_engine
from behavioral_engine.llm_client import generate_narrative

router = APIRouter(
    prefix="/simulate",
    tags=["Simulation"]
)

@router.post("/run")
def simulate_future_state(
    habits: HabitInput,
    horizon: str = Query(
        "6_months",
        enum=["1_month", "6_months", "1_year"]
    )
):
    # 1. Run deterministic behavioral engine
    result = run_behavioral_engine(
        habits=habits.model_dump(),
        horizon=horizon
    )

    # 2. Generate narrative using LLM (or fallback)
    narrative = generate_narrative(
    result["prompt"],
    result["states"]
    )


    # 3. Return only safe, user-facing data
    return {
        "states": result["states"],
        "narrative": narrative
    }
