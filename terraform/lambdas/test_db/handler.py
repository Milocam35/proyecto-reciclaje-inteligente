import pymysql
import os

def handler(event, context):
    try:
        conn = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            database=os.environ['DB_NAME'],
            connect_timeout=5
        )
        with conn.cursor() as cur:
            cur.execute("SELECT NOW();")
            result = cur.fetchone()
        conn.close()
        return {"status": "success", "mysql_time": str(result[0])}
    except Exception as e:
        return {"status": "error", "message": str(e)}
