import pyodbc

def get_connection():

    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=devsql02\\incredible;"
        "DATABASE=MandateRepository;"
        "Trusted_Connection=yes;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )

    return pyodbc.connect(conn_str)