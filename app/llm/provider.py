import time
from google import genai
from google.genai import types
import inspect
from app.core.config import settings

# debug: show which genai module is being used
print("genai module file", inspect.getfile(genai))

client = None

if settings.PROVIDER == "gemini":
    client = genai.Client(
        api_key=settings.MODEL_API_KEY,
        http_options=types.HttpOptions(api_version="v1")
    )

def generate_llm_response(messages):
    start = time.time()

    if settings.PROVIDER == "gemini":
        # Gemini doesn't use chat format like OpenAI
        prompt = messages[0]["content"] + "\n" + messages[1]["content"]

        response = client.models.generate_content(
            model=settings.MODEL_NAME,
            contents=prompt
        )

        latency = int((time.time() - start) * 1000)

        return {
            "content": response.text,
            "token_usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            },
            "latency": latency
        }