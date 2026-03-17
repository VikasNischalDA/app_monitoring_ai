from langchain_core.tools import tool
from db.sql_server import get_connection


@tool
def query_database(sql_query: str) -> str:
    """
    Execute a SQL query on SQL Server and return results.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql_query)

    columns = [column[0] for column in cursor.description]

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    cursor.close()
    conn.close()

    return str(result)