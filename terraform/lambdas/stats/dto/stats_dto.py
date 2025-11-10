from datetime import datetime

class StatsDTO:
    def __init__(
        self,
        id=None,
        fn=None,
        fp=None,
        vn=None,
        vp=None,
        precision_global=None,
        recall=None,
        f1_score=None,
        auc=None,
        fecha_creacion=None
    ):
        self.id = id

        # Validaciones numéricas
        for field_name, value in {
            "fn": fn,
            "fp": fp,
            "vn": vn,
            "vp": vp,
            "precision_global": precision_global,
            "recall": recall,
            "f1_score": f1_score,
            "auc": auc
        }.items():
            if value is not None and not isinstance(value, (int, float)):
                raise TypeError(f"El campo '{field_name}' debe ser numérico (int o float).")

        self.fn = fn
        self.fp = fp
        self.vn = vn
        self.vp = vp
        self.precision_global = precision_global
        self.recall = recall
        self.f1_score = f1_score
        self.auc = auc

        # Validación de fecha
        if fecha_creacion is not None:
            if isinstance(fecha_creacion, str):
                try:
                    # Acepta formato ISO (YYYY-MM-DDTHH:MM:SS)
                    fecha_creacion = datetime.fromisoformat(fecha_creacion)
                except ValueError:
                    # Acepta formato clásico (YYYY-MM-DD HH:MM:SS)
                    fecha_creacion = datetime.strptime(fecha_creacion, "%Y-%m-%d %H:%M:%S")
            elif not isinstance(fecha_creacion, datetime):
                raise TypeError("El campo 'fecha_creacion' debe ser una cadena o datetime.")
        else:
            fecha_creacion = datetime.now()

        self.fecha_creacion = fecha_creacion

    @staticmethod
    def from_dict(data: dict):
        """Crea un StatsDTO desde un diccionario (por ejemplo, un JSON recibido por la API)."""
        if not isinstance(data, dict):
            raise TypeError("El parámetro 'data' debe ser un diccionario.")

        return StatsDTO(
            id=data.get("id"),
            fn=data.get("fn"),
            fp=data.get("fp"),
            vn=data.get("vn"),
            vp=data.get("vp"),
            precision_global=data.get("precision_global"),
            recall=data.get("recall"),
            f1_score=data.get("f1_score"),
            auc=data.get("auc"),
            fecha_creacion=data.get("fecha_creacion")
        )

    def to_dict(self):
        """Convierte el DTO en un diccionario serializable (para respuesta JSON)."""
        return {
            "id": self.id,
            "fn": self.fn,
            "fp": self.fp,
            "vn": self.vn,
            "vp": self.vp,
            "precision_global": self.precision_global,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "auc": self.auc,
            "fecha_creacion": self.fecha_creacion
        }
