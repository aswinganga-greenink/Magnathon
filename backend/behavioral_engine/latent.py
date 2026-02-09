from behavioral_engine import config

def sleep_quality(L, S):
    return max(
        0.0,
        1 - (config.W_LATE_NIGHT * L + config.W_SLEEP_DISRUPTION * S + config.W_DISRUPTION_CONTINOUS * S)
    )


def cognitive_load(A, SQ):
    return min(
        1.0,
        config.W_APP_SWITCHING * A +
        config.W_SLEEP_AMPLIFIER * (1 - SQ)
    )



def habit_automaticity(L: float, A: float, P: float) -> float:
    return (L + A + P) / 3
