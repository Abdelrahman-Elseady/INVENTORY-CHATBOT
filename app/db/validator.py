def validate_sql(sql: str) -> bool:
    sql_lower = sql.strip().lower()

    if not sql_lower.startswith("select"):
        return False

    forbidden_keywords = ["drop", "delete", "update", "insert", "alter"]

    for keyword in forbidden_keywords:
        if keyword in sql_lower:
            return False

    return True