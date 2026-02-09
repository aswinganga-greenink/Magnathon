from behavioral_engine.time_model import apply_time_degradation
from behavioral_engine import config


def energy(SQ, CL, B, t):
    base = 1 - (
        config.ENERGY_SLEEP * (1 - SQ) +
        config.ENERGY_LOAD * CL
    )


    degraded = base - apply_time_degradation(base, t)

    recovery = B * min(
    config.MAX_BREAK_RECOVERY_ENERGY,
    1 - degraded
    )
    return max(0.0, min(1.0, degraded + recovery))



def focus(CL: float, HA: float, B: float, t: float) -> float:
    """
    Focus stability:
    - Degraded by cognitive load (primary)
    - Degraded by habit automaticity (secondary)
    - Restored by intentional breaks
    - Worsens non-linearly over time
    """
    base = 1 - (
        config.FOCUS_LOAD * CL +
        config.FOCUS_HABIT * HA
    )




    degraded = base - apply_time_degradation(base, t)

    recovery = B * min(
    config.MAX_BREAK_RECOVERY_FOCUS,
    1 - degraded
    )

    return max(0.0, min(1.0, degraded + recovery))



def emotional_regulation(SQ: float, CL: float, P: float, t: float) -> float:
    """
    Emotional regulation:
    - Strongly dependent on sleep quality
    - Moderately affected by cognitive load
    - Negatively affected by passive consumption
    - Degrades over time, but is slower to recover
    """
    base = 1 - (
        config.EMOTION_SLEEP * (1 - SQ) +
        config.EMOTION_LOAD * CL +
        config.EMOTION_PASSIVE * P
    )

    degraded = base - apply_time_degradation(base, t)

    return max(0.0, min(1.0, degraded))
