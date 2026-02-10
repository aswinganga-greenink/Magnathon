import google.generativeai as genai
import os
import dotenv

dotenv.load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key present: {bool(api_key)}")
genai.configure(api_key=api_key)

model_name = "gemini-flash-lite-latest"
print(f"Testing model: {model_name}")

try:
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Hello")
    print("Success:")
    print(response.text)
except Exception as e:
    print("Error:")
    print(e)
    print("\nAvailable models:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as list_e:
        print(f"Could not list models: {list_e}")
