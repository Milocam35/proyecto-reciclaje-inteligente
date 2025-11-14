from repositories.event_repository import EventRepository
from models.event_model import EventModel, TipoReal
from datetime import datetime
import math

class EventService:
    """
    Capa de servicio que encapsula la lógica de negocio relacionada con los eventos.
    """

    def __init__(self):
        self.repo = EventRepository()

    # ------------------------
    # 🟢 Crear un nuevo evento
    # ------------------------
    def create_event(self, dto):
        """
        Crea un evento nuevo y lo guarda en la base de datos.
        Valida campos obligatorios y calcula la duración automáticamente.
        """
        # Validaciones
        if not dto.horaClasificado:
            raise ValueError("El campo 'horaClasificado' es obligatorio.")
        if not dto.tipoClasificado:
            raise ValueError("El campo 'tipoClasificado' es obligatorio.")

        # Calcular la duración (en segundos)
        hora_clasificado = datetime.strptime(dto.horaClasificado, "%Y-%m-%d %H:%M:%S")
        hora_sincronizado = datetime.strptime(dto.horaSincronizado, "%Y-%m-%d %H:%M:%S")
        duracion = (hora_sincronizado - hora_clasificado).total_seconds()

        # Crear modelo de evento
        event = EventModel(
            horaClasificado=hora_clasificado,
            horaSincronizado=hora_sincronizado,
            duracion=duracion,
            rutaImagen=dto.rutaImagen,
            tipoClasificado=dto.tipoClasificado,
            tipoReal=dto.tipoReal if dto.tipoReal else TipoReal.NO_REVISADO.value,
            admin_id=dto.admin_id,
            confianza=dto.confianza
        )

        # Guardar en DB
        self.repo.insert_event(event)
        return {"message": "Evento creado correctamente"}

    # ------------------------
    # 🔵 Obtener todos los eventos
    # ------------------------
    def list_events(self):
        events = self.repo.get_all_events()
        return [event.to_dict() for event in events]

    # ------------------------
    # 🟡 Obtener eventos paginados
    # ------------------------
    def get_paginated_events(self, page: int = 1, page_size: int = 10):
        return self.repo.get_paginated_events(page, page_size)

    # ------------------------
    # 🟣 Obtener un evento por ID
    # ------------------------
    def get_event_by_id(self, event_id):
        event = self.repo.get_event_by_id(event_id)
        if not event:
            raise ValueError(f"No se encontró el evento con ID {event_id}")
        return event.to_dict()

    # ------------------------
    # 🟠 Actualizar tipoReal (clasificación real)
    # ------------------------
    def update_tipo_real(self, event_id, tipo_real):
        """
        Actualiza el tipo real del evento
        """
        # Obtener evento existente
        event = self.repo.get_event_by_id(event_id)
        if not event:
            raise ValueError(f"No existe el evento con ID {event_id}")
        
        if tipo_real not in [tipo.value for tipo in TipoReal]:
            raise ValueError("El tipo real proporcionado no es válido.")
        
        # Actualizar DB
        success = self.repo.update_event(event_id, tipo_real=tipo_real)
        if not success:
            raise RuntimeError("No se pudo actualizar el evento.")

    # ------------------------
    # Eliminar un evento por ID
    # ------------------------
    def delete_event(self, event_id):
        success = self.repo.delete_event(event_id)
        if not success:
            raise ValueError(f"No se pudo eliminar el evento con ID {event_id}")

