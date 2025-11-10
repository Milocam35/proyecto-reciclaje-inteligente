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
      - POST   /events           → crear evento
      - GET    /events           → listar eventos
      - GET    /events/{id}      → obtener evento por id
      - GET    /events (paginado)→ listar eventos (paginado)
      - PUT    /events/{id}/tipo → actualizar tipo real del evento
    """
    try:
        http_method = event.get("httpMethod")
        path = event.get("path", "")

        # POST /eventos
        if http_method == "POST" and path.endswith("/events"):
            return create_event(event)

        # GET /eventos
        elif http_method == "GET" and path.endswith("/events"):
            params = event.get("queryStringParameters") or {}

            if "page" in params or "page_size" in params:
                return get_paginated_events(event)
            else:
                return list_events()


        # GET /eventos/{id}
        elif http_method == "GET" and "/events/" in path:
            event_id = path.split("/")[-1]
            return get_event_by_id(event_id)

        # PUT /eventos/{id}/tipo
        elif http_method == "PUT" and path.endswith("/tipo"):
            event_id = path.split("/")[-2]
            return update_event_tipo(event, event_id)
        # DELETE /events/{id}
        elif http_method == "DELETE" and "/events/" in path:
            event_id = path.split("/")[-1]
            return delete_event(event)
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


# --- RUTA: GET /events/{id} ---
def get_event_by_id(event_id):
    result = service.get_event_by_id(event_id)
    return response(200, result)

# --- RUTA: GET /events (paginado) ---
def get_paginated_events(event):
    query_params = event.get("queryStringParameters") or {}
    page = int(query_params.get("page", 1))
    page_size = int(query_params.get("page_size", 10))
    result = service.get_paginated_events(page, page_size)
    return response(200, result)


# --- RUTA: PUT /events/{id}/tipo ---
def update_event_tipo(event):
    try:
        path_params = event.get("pathParameters", {})
        event_id = int(path_params.get("id"))
        body = json.loads(event.get("body", "{}"))
        tipo_real = body.get("tipoReal")

        if not tipo_real:
            return {"statusCode": 400, "body": json.dumps({"message": "Falta el campo tipoReal"})}

        service.update_tipo_real(event_id, tipo_real)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Evento {event_id} actualizado a tipo {tipo_real}"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }

# --- RUTA: DELETE /events/{id} ---
def delete_event(event):
    path_params = event.get("pathParameters", {})
    event_id = int(path_params.get("id"))
    service.delete_event(event_id)
    return response(200, {"message": f"Evento {event_id} eliminado correctamente"})

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
