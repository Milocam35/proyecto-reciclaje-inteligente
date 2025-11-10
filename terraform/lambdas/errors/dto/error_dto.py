class ErrorDto:
    def __init__(self, id=None, hora=None, fuente=None, message=None, event_id=None):
        self.id = id
        self.hora = hora
        self.fuente = fuente
        self.message = message
        self.event_id = event_id
    
    @staticmethod
    def from_dict(data: dict):
        """Crea un EventDTO desde un diccionario (por ejemplo, un JSON recibido de API Gateway)."""
        if not isinstance(data, dict):
            raise TypeError("El parámetro 'data' debe ser un diccionario.")
        return ErrorDto(
            id=data.get("id"),
            hora=data.get("hora"),
            fuente=data.get("fuente"),
            message=data.get("message"),
            event_id=data.get("event_id")
        )
    
    def to_dict(self):
        """Convierte el DTO en un diccionario serializable para enviar como respuesta JSON."""
        return {
            "id": self.id,
            "hora": self.hora,
            "fuente": self.fuente,
            "message": self.message,
            "event_id": self.event_id
        }