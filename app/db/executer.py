from app.db.connection import get_connection

def execute_query(query: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    results = []
    for row in rows:
        results.append(dict(zip(columns, row)))

    cursor.close()
    conn.close()

    return results