from enum import Enum
from models.event_model import TipoClasificado, TipoReal

class EventDTO:
    def __init__(
        self,
        id=None,
        horaClasificado=None,
        horaSincronizado=None,
        duracion=None,
        rutaImagen=None,
        tipoClasificado=None,
        tipoReal=TipoReal.NO_REVISADO.value,
        admin_id=None,
        confianza=None
    ):
        self.id = id
        self.horaClasificado = horaClasificado
        self.horaSincronizado = horaSincronizado
        self.duracion = duracion
        self.rutaImagen = rutaImagen

        # Validación de tipoClasificado
        if tipoClasificado is not None:
            valid_values = [e.value for e in TipoClasificado]
            if tipoClasificado not in valid_values:
                raise ValueError(f"TipoClasificado inválido: {tipoClasificado}")
        self.tipoClasificado = tipoClasificado

        # Validación de tipoReal
        if tipoReal is not None:
            valid_values = [e.value for e in TipoReal]
            if tipoReal not in valid_values:
                raise ValueError(f"TipoReal inválido: {tipoReal}")
        self.tipoReal = tipoReal or TipoReal.NO_REVISADO.value

        self.admin_id = admin_id
        self.confianza = confianza

    @staticmethod
    def from_dict(data: dict):
        """Crea un EventDTO desde un diccionario (por ejemplo, un JSON recibido de API Gateway)."""
        if not isinstance(data, dict):
            raise TypeError("El parámetro 'data' debe ser un diccionario.")

        return EventDTO(
            id=data.get("id"),
            horaClasificado=data.get("horaClasificado"),
            horaSincronizado=data.get("horaSincronizado"),
            duracion=data.get("duracion"),
            rutaImagen=data.get("rutaImagen"),
            tipoClasificado=data.get("tipoClasificado"),
            tipoReal=data.get("tipoReal"),
            admin_id=data.get("admin_id"),
            confianza=data.get("confianza")
        )

    def to_dict(self):
        """Convierte el DTO en un diccionario serializable para enviar como respuesta JSON."""
        return {
            "id": self.id,
            "horaClasificado": self.horaClasificado,
            "horaSincronizado": self.horaSincronizado,
            "duracion": self.duracion,
            "rutaImagen": self.rutaImagen,
            "tipoClasificado": self.tipoClasificado,
            "tipoReal": self.tipoReal,
            "admin_id": self.admin_id,
            "confianza": self.confianza
        }

