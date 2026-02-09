def dominant_issue(states: dict) -> str:
    if states["sleep"] == "DEPRIVED":
        return "sleep_deprivation"
    if states["focus"] == "SCATTERED":
        return "attention_fragmentation"
    return "cognitive_strain"