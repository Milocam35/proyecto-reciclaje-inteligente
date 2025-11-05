import pymysql
import os
import json

def handler(event, context):
    try:
        # === Conexión a la base de datos ===
        connection = pymysql.connect(
            host=os.environ["DB_HOST"].split(':')[0],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            database=os.environ.get("DB_NAME", "reciclaje_db"),
            connect_timeout=5
        )

        # === Ejemplo: consulta de usuarios ===
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM users LIMIT 10;")
            results = cursor.fetchall()

        connection.close()

        # === Respuesta exitosa ===
        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "ok",
                "message": "Consulta ejecutada correctamente",
                "results": results
            })
        }

    except pymysql.MySQLError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": f"Error en MySQL: {str(e)}"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": str(e)
            })
        }
