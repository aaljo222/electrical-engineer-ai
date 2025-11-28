import psycopg2
import os

def get_conn():
    url = os.environ["DATABASE_URL"]  # postgres://xxxx
    return psycopg2.connect(url)

def fetch_one(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params or ())
    row = cur.fetchone()
    conn.close()
    return row

def fetch_all(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params or ())
    rows = cur.fetchall()
    conn.close()
    return rows

# ⭐⭐⭐ 여기 추가 ⭐⭐⭐
def execute(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    conn.close()
