import json
from services.event_service import EventService
from dto.event_dto import EventDTO
import traceback

service = EventService()

def handler(event, context):

    print("==== EVENTO RECIBIDO ====")
    print(json.dumps(event))

    """
    Controlador principal de la API de Eventos.
    Rutas:
      - POST   /eventos           → crear evento
      - GET    /eventos           → listar eventos
      - GET    /eventos/{id}      → obtener evento por id
      - PUT    /eventos/{id}/tipo → actualizar tipo real del evento
    """
    try:
        http_method = event.get("httpMethod")
        path = event.get("path", "")

        # POST /eventos
        if http_method == "POST" and path.endswith("/events"):
            return create_event(event)

        # GET /eventos
        elif http_method == "GET" and path.endswith("/events"):
            return list_events()

        # GET /eventos/{id}
        elif http_method == "GET" and "/events/" in path:
            event_id = path.split("/")[-1]
            return get_event_by_id(event_id)

        # PUT /eventos/{id}/tipo
        elif http_method == "PUT" and path.endswith("/tipo"):
            event_id = path.split("/")[-2]
            return update_event_tipo(event, event_id)

        else:
            return response(404, {"message": "Ruta no encontrada"})

    except Exception as e:
        print("==== ERROR DETECTADO ====")
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


# --- RUTA: POST /eventos ---
def create_event(event):
    body = json.loads(event.get("body", "{}"))
    dto = EventDTO.from_dict(body)
    result = service.create_event(dto)
    return response(201, result)


# --- RUTA: GET /eventos ---
def list_events():
    result = service.list_events()
    return response(200, result)


# --- RUTA: GET /eventos/{id} ---
def get_event_by_id(event_id):
    result = service.get_event_by_id(event_id)
    return response(200, result)


# --- RUTA: PUT /eventos/{id}/tipo ---
def update_event_tipo(event, event_id):
    body = json.loads(event.get("body", "{}"))
    tipo_real = body.get("tipoReal")
    result = service.update_event_real_type(event_id, tipo_real)
    return response(200, result)


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
