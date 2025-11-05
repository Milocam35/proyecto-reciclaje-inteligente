import pymysql
import os

def handler(event, context):
    try:
        # Leer el esquema SQL desde el archivo local dentro del ZIP
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r") as f:
            sql_script = f.read()

        statements = [s.strip() for s in sql_script.split(';') if s.strip()]

        # Conexión a la base de datos
        conn = pymysql.connect(
            host=os.environ['DB_HOST'].split(':')[0],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            database=os.environ['DB_NAME'],
            connect_timeout=5
        )

        with conn.cursor() as cursor:
            for stmt in statements:
                print(f"🧩 Ejecutando: {stmt}")
                cursor.execute(stmt)

        conn.commit()
        conn.close()

        return {"status": "ok", "executed": len(statements)}

    except Exception as e:
        return {"status": "error", "message": str(e)}
