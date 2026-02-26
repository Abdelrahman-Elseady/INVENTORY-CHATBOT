import json
from app.llm.prompt_builder import build_messages
from app.llm.provider import generate_llm_response

def handle_chat(message: str):

    messages = build_messages(message)

    llm_result = generate_llm_response(messages)

    content = llm_result["content"]

    # strip markdown code fences if present (````json ... ```)
    text = content.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        # drop opening fence
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        # drop closing fence
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    try:
        parsed = json.loads(text)
    except Exception as e:
        # provide context for debugging
        raise ValueError(f"failed to parse LLM output as JSON: {e}\nraw_content={content}")

    return {
        "answer": parsed["natural_language_answer"],
        "sql": parsed["sql_query"],
        "latency": llm_result["latency"],
        "token_usage": llm_result["token_usage"]
    }