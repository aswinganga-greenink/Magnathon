import os
import re
import google.generativeai as genai
import dotenv

dotenv.load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use a strong but safe model
_MODEL = genai.GenerativeModel("gemma-3-12b-it")

# Safety patterns
_ADVICE_PATTERNS = [
    r"\byou should\b",
    r"\btry to\b",
    r"\bi recommend\b",
    r"\bconsider\b",
]

_MEDICAL_PATTERNS = [
    r"\bdiagnos",
    r"\bdisorder\b",
    r"\bdepression\b",
    r"\banxiety\b",
]

MAX_WORDS = 120


def _contains_forbidden_language(text: str) -> bool:
    lowered = text.lower()
    for p in _ADVICE_PATTERNS + _MEDICAL_PATTERNS:
        if re.search(p, lowered):
            return True
    return False


def _word_count(text: str) -> int:
    return len(text.split())


def generate_narrative(
    prompt: str,
    states: dict,
    *,
    temperature: float = 0.7
) -> str:
    try:
        response = _MODEL.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 3000,
            },
        )

        text = response.text.strip()

        if _word_count(text) > MAX_WORDS:
            return generate_narrative(prompt, states, temperature=0.4)

        if _contains_forbidden_language(text):
            return generate_narrative(prompt, states, temperature=0.3)

        return text

    except Exception as e:
        # optional debug during dev
        return {"LLM ERROR:" : repr(e)}




def _fallback_narrative(prompt: str) -> str:
    lines = []

    if "Sleep: DEPRIVED" in prompt:
        lines.append("Sleep feels inconsistent, and mornings start with a sense of heaviness.")
    elif "Sleep: STRAINED" in prompt:
        lines.append("Sleep happens, but it doesn’t always feel fully restorative.")
    else:
        lines.append("Sleep feels stable and predictable.")

    if "Focus: LOW" in prompt:
        lines.append("Attention drifts easily, and staying with one task takes effort.")
    elif "Focus: MODERATE" in prompt:
        lines.append("Focus comes in waves, with moments of clarity and moments of distraction.")
    else:
        lines.append("Focus feels steady and intentional.")

    if "Energy: LOW" in prompt:
        lines.append("Energy drops earlier in the day, even without heavy physical strain.")
    elif "Energy: MODERATE" in prompt:
        lines.append("Energy is usable, though it fluctuates across the day.")
    else:
        lines.append("Energy feels sufficient and well-supported.")

    if "Emotional balance: LOW" in prompt:
        lines.append("Emotional balance feels harder to maintain under pressure.")
    elif "Emotional balance: MODERATE" in prompt:
        lines.append("Emotional balance holds, though stress is noticeable at times.")
    else:
        lines.append("Emotional balance feels stable.")

    return " ".join(lines)
