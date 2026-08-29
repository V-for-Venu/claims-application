import sqlite3

import pandas as pd

db_path = r"G:\learning_v\FastAPI\claims-application\basic-app\new_database\claims.db"
watermark_file = "watermark.txt"


def get_watermark():
    with open(watermark_file) as watermark:
        return watermark.read().strip()


def extract_claims():
    watermark = get_watermark()

    conn = sqlite3.connect(db_path)
    query = f"""
    SELECT * FROM claims WHERE
    ClaimAuditTime > '{watermark}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    if df.empty:
        print("== Inside Extract Task -- NO NEW DATA FOUND ==")

    return df
