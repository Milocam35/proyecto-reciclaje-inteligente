from datetime import datetime

class StatsModel:
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
        self.fn = fn
        self.fp = fp
        self.vn = vn
        self.vp = vp
        self.precision_global = precision_global
        self.recall = recall
        self.f1_score = f1_score
        self.auc = auc
        self.fecha_creacion = self._parse_datetime(fecha_creacion) or datetime.now()

    @staticmethod
    def _parse_datetime(value):
        """Convierte un string a datetime si es necesario."""
        if isinstance(value, str):
            try:
                # Acepta formato ISO (YYYY-MM-DDTHH:MM:SS)
                return datetime.fromisoformat(value)
            except ValueError:
                # Acepta formato clásico (YYYY-MM-DD HH:MM:SS)
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return value

    def to_dict(self):
        """Convierte el modelo a diccionario (por ejemplo, para devolver en JSON)."""
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
            "fecha_creacion": self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def from_dict(data):
        """Crea una instancia del modelo desde un diccionario (por ejemplo, fila de base de datos)."""
        return StatsModel(
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
