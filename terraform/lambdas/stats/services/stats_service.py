from datetime import datetime
from events.repositories.event_repository import EventRepository
from stats.repositories.stats_repository import StatsRepository
from stats.models.stats_model import StatsModel
from stats.dto.stats_dto import StatsDTO
from events.models.event_model import TipoReal  # Enum de los tipos
import math

class StatsService:
    """
    Servicio que calcula y gestiona las estadísticas de clasificación
    basadas en los eventos almacenados en la BD.
    """

    def __init__(self):
        self.event_repo = EventRepository()
        self.stats_repo = StatsRepository()

    # ------------------------
    # Calcular estadísticas desde eventos
    # ------------------------
    def generate_stats(self):
        """
        Calcula métricas globales (VP, FP, VN, FN, precisión, recall, f1, etc.)
        a partir de los eventos en la base de datos.
        """

        # Obtener todos los eventos
        events = self.event_repo.get_all_events()
        if not events:
            raise ValueError("No hay eventos disponibles para generar estadísticas.")

        # Inicializar contadores
        vp = vn = fp = fn = 0

        for event in events:
            clasificado = event.tipoClasificado.value
            real = event.tipoReal.value

            # Solo contamos si el tipo real fue revisado
            if real == TipoReal.NO_REVISADO.value:
                continue

            if clasificado == "reciclable" and real == "reciclable":
                vp += 1
            elif clasificado == "reciclable" and real == "no_reciclable":
                fp += 1
            elif clasificado == "no_reciclable" and real == "reciclable":
                fn += 1
            elif clasificado == "no_reciclable" and real == "no_reciclable":
                vn += 1

        # Calcular métricas
        total = vp + vn + fp + fn
        precision_global = (vp + vn) / total if total > 0 else 0
        recall = vp / (vp + fn) if (vp + fn) > 0 else 0
        precision = vp / (vp + fp) if (vp + fp) > 0 else 0
        f1_score = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0 else 0
        )

        # Como no hay probabilidades, el AUC puede definirse como una métrica derivada simple
        auc = (recall + precision) / 2

        # Crear modelo de estadística
        stat = StatsModel(
            vp=vp,
            vn=vn,
            fp=fp,
            fn=fn,
            precision_global=precision_global,
            recall=recall,
            f1_score=f1_score,
            auc=auc,
            fecha_creacion=datetime.now()
        )

        # Guardar en BD
        self.stats_repo.insert_stats(stat)

        return {
            "message": "Estadísticas generadas correctamente",
            "data": stat.to_dict()
        }

    # ------------------------
    # Consultar estadísticas por rango de fechas
    # ------------------------
    def get_stats_by_range(self, fecha_inicio, fecha_fin):
        """
        Devuelve todas las estadísticas entre dos fechas.
        """
        return self.stats_repo.get_stats_by_range(fecha_inicio, fecha_fin)


    # ------------------------
    # Listar todas las estadísticas
    # ------------------------
    def list_stats(self):
        """
        Devuelve todas las estadísticas almacenadas en la base de datos.
        """
        stats = self.stats_repo.get_all_stats()
        return [s.to_dict() for s in stats]


    # ------------------------
    # Obtener estadística específica por ID
    # ------------------------
    def get_stats_by_id(self, stats_id):
        """
        Devuelve una estadística específica por su ID.
        """
        stat = self.stats_repo.get_stats_by_id(stats_id)
        if stat:
            return stat.to_dict()
        return None