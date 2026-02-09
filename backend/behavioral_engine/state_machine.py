def level(x: float):
    if x >= 0.7:
        return "HIGH"
    elif x >= 0.4:
        return "MODERATE"
    else:
        return "LOW"

def sleep_state(SQ):
    if SQ < 0.4:
        return "DEPRIVED"
    elif SQ < 0.7:
        return "STRAINED"
    else:
        return "RESTED"
