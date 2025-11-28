import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_conn():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    # Supabase Postgres 접속 정보 생성
    # URL 형태: https://xxxxx.supabase.co
    host = url.replace("https://", "").replace(".supabase.co", ".supabase.co")

    return psycopg2.connect(
        host=f"db.{host}",
        user="postgres",
        password=key,
        database="postgres",
        port=5432,
        cursor_factory=RealDictCursor
    )


def fetch_one(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params or ())
    row = cur.fetchone()
    conn.close()
    return row


def execute(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    conn.close()
