from datetime import datetime
from enum import Enum

class TipoReal(Enum):
    NO_REVISADO = "noRevisado"
    RECICLABLE = "reciclable"
    NO_RECICLABLE = "noReciclable"
    ORGANICO = "organico"

class TipoClasificado(Enum):
    RECICLABLE = "reciclable"
    NO_RECICLABLE = "noReciclable"
    ORGANICO = "organico"

class EventModel:
    def __init__(
        self,
        id=None,
        horaClasificado=None,
        horaSincronizado=None,
        duracion=None,
        rutaImagen=None,
        tipoClasificado=None,
        tipoReal=TipoReal.NO_REVISADO,
        admin_id=None,
        confianza=None
    ):
        self.id = id
        self.horaClasificado = self._parse_datetime(horaClasificado) or datetime.now()
        self.horaSincronizado = self._parse_datetime(horaSincronizado) or datetime.now()
        self.duracion = duracion
        self.rutaImagen = rutaImagen

        # Convertir strings a enums (si vienen como texto)
        if tipoClasificado:
            self.tipoClasificado = (
                tipoClasificado if isinstance(tipoClasificado, TipoClasificado)
                else TipoClasificado(tipoClasificado)
            )
        else:
            self.tipoClasificado = None

        if tipoReal:
            self.tipoReal = (
                tipoReal if isinstance(tipoReal, TipoReal)
                else TipoReal(tipoReal)
            )
        else:
            self.tipoReal = TipoReal.NO_REVISADO

        self.admin_id = admin_id
        self.confianza = confianza

    @staticmethod
    def _parse_datetime(value):
        """Convierte string a datetime si es necesario."""
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return value

    def to_dict(self):
        """Convierte el modelo a diccionario (por ejemplo, para respuestas JSON)."""
        return {
            "id": self.id,
            "horaClasificado": self.horaClasificado.strftime("%Y-%m-%d %H:%M:%S"),
            "horaSincronizado": self.horaSincronizado.strftime("%Y-%m-%d %H:%M:%S"),
            "duracion": self.duracion,
            "rutaImagen": self.rutaImagen,
            "tipoClasificado": self.tipoClasificado.value if self.tipoClasificado else None,
            "tipoReal": self.tipoReal.value if self.tipoReal else None,
            "admin_id": self.admin_id,
            "confianza": self.confianza
        }

    @staticmethod
    def from_dict(data):
        """Crea una instancia del modelo desde un diccionario (por ejemplo, fila de la base de datos)."""
        return EventModel(
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
