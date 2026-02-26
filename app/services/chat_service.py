import time
from app.db.validator import validate_sql

def generate_sql_response(message: str):
    start_time = time.time()

    msg = message.lower()

    if "how many assets" in msg:
        sql = """
        SELECT COUNT(*) AS AssetCount
        FROM Assets
        WHERE Status <> 'Disposed';
        """
        answer = "You have {value} assets in your inventory."

    elif "assets by site" in msg:
        sql = """
        SELECT s.SiteName, COUNT(*) AS AssetCount
        FROM Assets a
        JOIN Sites s ON s.SiteId = a.SiteId
        WHERE a.Status <> 'Disposed'
        GROUP BY s.SiteName
        ORDER BY AssetCount DESC;
        """
        answer = "Here is the asset count by site."

    elif "open purchase orders" in msg:
        sql = """
        SELECT PONumber, PODate, Status
        FROM PurchaseOrders
        WHERE Status = 'Open';
        """
        answer = "Here are your open purchase orders."

    else:
        sql = "SELECT 'Unknown question' AS Message;"
        answer = "Sorry, I do not understand the question yet."

    # Validate SQL
    if not validate_sql(sql):
        return {
            "natural_language_answer": "Unsafe query detected.",
            "sql_query": "",
            "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "latency_ms": 0,
            "provider": "manual",
            "model": "rule-based",
            "status": "error"
        }

    latency = float((time.time() - start_time) * 1000)

    return {
        "natural_language_answer": answer,
        "sql_query": sql.strip(),
        "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "latency_ms": latency,
        "provider": "manual",
        "model": "rule-based",
        "status": "ok"
    }