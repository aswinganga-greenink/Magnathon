from behavioral_engine.inputs import normalize
from behavioral_engine.latent import (
    sleep_quality,
    cognitive_load,
    habit_automaticity
)
from behavioral_engine.time_model import time_multiplier
from behavioral_engine.outcomes import (
    energy,
    focus,
    emotional_regulation
)
from behavioral_engine.state_machine import (
    sleep_state,
    level
)
from behavioral_engine.framing import dominant_issue
from behavioral_engine.prompt import future_self_prompt



def run_behavioral_engine(habits: dict, horizon: str) -> dict:
    """
    Canonical behavioral simulation pipeline.
    This is the ONLY place where the system is connected.
    """

    # 1. Normalize inputs
    L = normalize(habits["late_night_usage"])
    A = normalize(habits["app_switching"])
    P = normalize(habits["passive_consumption"])
    S = normalize(habits["sleep_disruption"])
    B = normalize(habits["intentional_breaks"])

    # 2. Latent variables (science layer)
    SQ = sleep_quality(L, S)
    CL = cognitive_load(A, SQ)
    HA = habit_automaticity(L, A, P)

    # 3. Time dynamics
    t = time_multiplier(horizon)

    # 4. Outcomes (still numeric, internal)
    E = energy(SQ, CL, B, t)
    F = focus(CL, HA, B, t)
    ER = emotional_regulation(SQ, CL, P, t)

    # 5. Discrete states (human-meaningful)
    states = {
        "sleep": sleep_state(SQ),
        "energy": level(E),
        "focus": level(F),
        "emotion": level(ER)
    }

    # 6. Decision framing (non-language reasoning)
    frame = {
        "sleep_state": states["sleep"],
        "energy_state": states["energy"],
        "focus_state": states["focus"],
        "emotion_state": states["emotion"],
        "dominant_issue": dominant_issue(states),
        "horizon": horizon
    }

    # 7. Prompt generation (LLM-safe)
    prompt = future_self_prompt(frame)

    return {
        "latent": {
            "sleep_quality": SQ,
            "cognitive_load": CL,
            "habit_automaticity": HA
        },
        "outcomes": {
            "energy": E,
            "focus": F,
            "emotional_regulation": ER
        },
        "states": states,
        "frame": frame,
        "prompt": prompt
    }
