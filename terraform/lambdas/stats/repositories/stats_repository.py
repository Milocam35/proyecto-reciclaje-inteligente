import pymysql
import os
from models.stats_model import StatsModel

class StatsRepository:
    """
    Repositorio encargado de las operaciones CRUD sobre la tabla Estadistica.
    """

    def __init__(self):
        self.host = os.environ["DB_HOST"].split(":")[0]
        self.user = os.environ["DB_USER"]
        self.password = os.environ["DB_PASS"]
        self.database = os.environ.get("DB_NAME", "reciclaje_db")

    def _get_connection(self):
        """Crea y devuelve una conexión a la base de datos MySQL."""
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            connect_timeout=5,
            cursorclass=pymysql.cursors.DictCursor
        )

    # ------------------------
    # 🟢 Insertar una nueva estadística
    # ------------------------
    def insert_stat(self, stat: StatsModel):
        query = """
        INSERT INTO Estadistica (
            fn, fp, vn, vp,
            precision_global, recall, f1_score, auc, fecha_creacion
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            stat.fn,
            stat.fp,
            stat.vn,
            stat.vp,
            stat.precision_global,
            stat.recall,
            stat.f1_score,
            stat.auc,
            stat.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
        )

        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
            conn.commit()
        finally:
            conn.close()

    # ------------------------
    # 🔵 Obtener todas las estadísticas
    # ------------------------
    def get_all_stats(self):
        query = "SELECT * FROM Estadistica ORDER BY fecha_creacion DESC;"
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return [StatsModel.from_dict(row) for row in results]
        finally:
            conn.close()

    # ------------------------
    # 🟣 Obtener estadística por ID
    # ------------------------
    def get_stat_by_id(self, stat_id: int):
        query = "SELECT * FROM Estadistica WHERE id = %s;"
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (stat_id,))
                row = cursor.fetchone()
                return StatsModel.from_dict(row) if row else None
        finally:
            conn.close()


    # ------------------------
    # 🟠 Consultar estadísticas por rango de fechas
    # ------------------------
    def get_stats_by_range(self, fecha_inicio, fecha_fin):
        query = """
        SELECT * FROM Estadistica
        WHERE fecha_creacion BETWEEN %s AND %s
        ORDER BY fecha_creacion DESC;
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (fecha_inicio, fecha_fin))
                results = cursor.fetchall()
                return [StatsModel.from_dict(row).to_dict() for row in results]
        finally:
            conn.close()