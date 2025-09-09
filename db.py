import psycopg2
import pandas as pd

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="tennis_db",
        user="postgres",            # change if different
        password="Tthiri!21@003"    # 🔑 your pgAdmin password
    )

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
