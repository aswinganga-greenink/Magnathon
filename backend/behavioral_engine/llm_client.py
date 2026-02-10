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

MAX_WORDS = 300


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
) -> dict:
    try:
        print(f"DEBUG: Generating narrative with model {_MODEL.model_name}...")
        # Update prompt to request JSON
        json_prompt = (
            f"{prompt}\n\n"
            "Format your response as a valid JSON object with two keys:\n"
            "- 'title': A creative, short 3-5 word persona title based on the habits (e.g., 'The Restless Achiever').\n"
            "- 'narrative': The first-person narrative as requested.\n"
            "Do NOT use Markdown formatting for the JSON."
        )

        response = _MODEL.generate_content(
            json_prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 3000,
            },
        )
        print(f"DEBUG: AI Response received. Candidate safety ratings: {response.candidates[0].safety_ratings if response.candidates else 'No candidates'}")
        
        text = response.text.strip()
        print(f"DEBUG: AI Text length: {len(text)}")

        if _word_count(text) > MAX_WORDS:
            print("DEBUG: Word count too high, retrying...")
            return generate_narrative(prompt, states, temperature=0.4)

        if _contains_forbidden_language(text):
            print("DEBUG: Forbidden language detected, retrying...")
            return generate_narrative(prompt, states, temperature=0.3)

        import json
        try:
            # Clean up markdown code blocks if present
            clean_text = text
            if "```" in clean_text:
                clean_text = clean_text.replace("```json", "").replace("```", "").strip()
            
            # Ensure we only try to parse the JSON object part
            start = clean_text.find("{")
            end = clean_text.rfind("}")
            if start != -1 and end != -1:
                clean_text = clean_text[start:end+1]

            return json.loads(clean_text)
        except json.JSONDecodeError:
             # Fallback if valid JSON isn't returned
             print("DEBUG: Failed to parse JSON, returning raw text as narrative")
             return {"title": "Future Persona", "narrative": text}

    except Exception as e:
        print(f"DEBUG: LLM Exception: {e}")
        # optional debug during dev
        return {"title": "Simulation Error", "narrative": f"Simulation generated, but AI narrative failed: {repr(e)}"}




def _fallback_narrative(prompt: str) -> dict:
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

    return {"title": "Projected Self", "narrative": " ".join(lines)}
