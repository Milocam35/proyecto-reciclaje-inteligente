from datetime import datetime
class ErrorModel:
    def __init__(self, id=None, hora=None, fuente=None, mensaje=None, event_id=None):
        self.id = id
        self.hora = self.__parse_datetime(hora) or datetime.now()
        self.fuente = fuente
        self.mensaje = mensaje
        self.event_id = event_id

    def __parse_datetime(self, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return value
    
    @staticmethod
    def from_dict(data: dict):
        """Crea un ErrorModel desde un diccionario (por ejemplo, un JSON recibido de API Gateway)."""
        if not isinstance(data, dict):
            raise TypeError("El parámetro 'data' debe ser un diccionario.")
        return ErrorModel(
            id=data.get("id"),
            hora=data.get("hora"),
            fuente=data.get("fuente"),
            mensaje=data.get("mensaje"),
            event_id=data.get("event_id")
        )