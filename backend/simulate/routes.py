from fastapi import APIRouter, Query, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
import json
from datetime import datetime

from simulate.validate import HabitInput
from behavioral_engine.engine import run_behavioral_engine
from behavioral_engine.llm_client import generate_narrative
from database import get_session
from models import User, Simulation
from auth.security import get_current_user

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
    ),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # 0. Update user display name if provided (first-time setup)
    if habits.display_name:
        current_user.full_name = habits.display_name
        session.add(current_user)
        session.commit()
        session.refresh(current_user)

    # 1. Run deterministic behavioral engine
    result = run_behavioral_engine(
        habits=habits.model_dump(exclude={"display_name"}),
        horizon=horizon
    )

    # 2. Generate narrative using LLM (or fallback)
    # 2. Generate narrative using LLM (or fallback)
    llm_output = generate_narrative(
        result["prompt"],
        states=result["states"]
    )
    
    # Handle legacy string return in case of weird fallback (though updated code returns dict)
    if isinstance(llm_output, str):
        llm_output = {"title": "Future Persona", "narrative": llm_output}

    final_result = {
        "states": result["states"],
        "narrative": llm_output.get("narrative", "No narrative generated."),
        "title": llm_output.get("title", "My Future Self"),
        "frame": {"horizon": horizon},
        "timestamp": datetime.now().isoformat()
    }

    # 3. Save to Database
    simulation = Simulation(
        user_id=current_user.id,
        habits=json.dumps(habits.model_dump()),
        result=json.dumps(final_result)
    )
    session.add(simulation)
    session.commit()
    session.refresh(simulation)

    return final_result

@router.get("/history")
def get_simulation_history(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Fetch simulations for current user ordered by creation time
    simulations = session.exec(
        select(Simulation).where(Simulation.user_id == current_user.id).order_by(Simulation.created_at.desc())
    ).all()
    
    history = []
    for sim in simulations:
        data = sim.result_dict
        # Ensure timestamp matches creation time if needed, or use DB time
        if "timestamp" not in data:
            data["timestamp"] = sim.created_at.isoformat()
        history.append(data)
        
    return history
