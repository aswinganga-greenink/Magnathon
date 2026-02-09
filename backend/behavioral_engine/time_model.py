import math
from behavioral_engine import config

TIME_HORIZONS = {
    "1_month": 0.25,
    "6_months": 0.65,
    "1_year": 1.0
}

def time_multiplier(horizon: str) -> float:
    return TIME_HORIZONS[horizon]


def compound(effect: float, time_factor: float) -> float:
    """
    Non-linear time compounding with saturation.
    """
    return effect * math.log1p(1 + 4 * time_factor)


def apply_time_degradation(base: float, time_factor: float) -> float:
    """
    Apply time degradation only after tolerance threshold.
    """
    deficit = max(
        0.0,
        (1 - base) - config.COMPOUNDING_THRESHOLD
    )
    return compound(deficit, time_factor)
