import json
from services.stats_service import StatsService
import traceback

service = StatsService()

def handler(event, context):
    """
    Controlador principal de la API de Estadísticas.
    Rutas:
      - POST /stats           → calcular y guardar estadísticas
      - GET  /stats           → listar estadísticas
      - GET  /stats/{id}      → obtener estadísticas por ID
    """
    print("==== EVENTO RECIBIDO ====")
    print(json.dumps(event))

    try:
        http_method = event.get("httpMethod")
        path = event.get("path", "")

        # POST /stats
        if http_method == "POST" and path.endswith("/stats"):
            return create_stats()

        # GET /stats
        elif http_method == "GET" and path.endswith("/stats"):
            return list_stats()

        # GET /stats/{id}
        elif http_method == "GET" and "/stats/" in path:
            stats_id = path.split("/")[-1]
            return get_stats_by_id(stats_id)

        else:
            return response(404, {"message": "Ruta no encontrada"})

    except Exception as e:
        print("==== ERROR DETECTADO EN STATS HANDLER ====")
        traceback.print_exc()
        return response(500, {"error": str(e)})


# --- RUTA: POST /stats ---
def create_stats():
    """
    Llama al servicio para recalcular las métricas globales (precision, recall, etc.)
    a partir de los eventos existentes y guarda el resultado.
    """
    result = service.generate_stats()
    return response(201, result)


# --- RUTA: GET /stats ---
def list_stats():
    result = service.list_stats()
    return response(200, result)


# --- RUTA: GET /stats/{id} ---
def get_stats_by_id(stats_id):
    result = service.get_stats_by_id(stats_id)
    if result:
        return response(200, result)
    else:
        return response(404, {"message": "Estadística no encontrada"})


# --- Helper ---
def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }