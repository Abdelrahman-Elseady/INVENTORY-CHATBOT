import json
from app.llm.prompt_builder import build_messages
from app.llm.provider import generate_llm_response
from app.db.validator import validate_sql
from app.db.executer import execute_query


def handle_chat(message: str):
    # Step 1: Generate SQL from user message
    messages = build_messages(message)
    llm_result = generate_llm_response(messages)

    content = llm_result["content"]

    # strip markdown code fences if present (```json ... ```)
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

    sql_query = parsed["sql_query"]
    initial_answer = parsed["natural_language_answer"]

    # Step 2: Validate SQL
    if not validate_sql(sql_query):
        return {
            "answer": "I cannot execute this query as it contains unsafe SQL operations.",
            "sql": sql_query,
            "latency": llm_result["latency"],
            "token_usage": llm_result["token_usage"]
        }

    # Step 3: Execute SQL and get results
    try:
        db_results = execute_query(sql_query)
    except Exception as e:
        return {
            "answer": f"Database error: {str(e)}",
            "sql": sql_query,
            "latency": llm_result["latency"],
            "token_usage": llm_result["token_usage"]
        }

    # Step 4: Format the result into a natural language answer
    if db_results:
        # For COUNT queries, ignore the LLM wording and generate a clear sentence
        if "COUNT" in sql_query.upper():
            first_row = db_results[0]
            count_value = list(first_row.values())[0]
            # build a grammatically correct phrase
            noun = "customer" if count_value == 1 else "customers"
            verb = "is" if count_value == 1 else "are"
            final_answer = f"There {verb} {count_value} {noun} in the system."
        else:
            # For other queries, include the raw results
            final_answer = f"{initial_answer}\n\nResults: {json.dumps(db_results, indent=2)}"
    else:
        final_answer = initial_answer + " (No results found)"

    return {
        "answer": final_answer,
        "sql": sql_query,
        "latency": llm_result["latency"],
        "token_usage": llm_result["token_usage"]
    }