import pymysql
import os
from models.event_model import EventModel
from models.event_model import TipoReal

class EventRepository:
    """
    Repositorio encargado de gestionar las operaciones CRUD de la tabla Evento.
    """

    def __init__(self):
        # Configuración de conexión obtenida desde variables de entorno del Lambda
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
    # 🟢 Crear un nuevo evento
    # ------------------------
    def insert_event(self, event: EventModel):
        query = """
        INSERT INTO Evento (
            horaClasificado, horaSincronizado, duracion,
            rutaImagen, tipoClasificado, tipoReal,
            admin_id, confianza
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            event.horaClasificado.strftime("%Y-%m-%d %H:%M:%S"),
            event.horaSincronizado.strftime("%Y-%m-%d %H:%M:%S"),
            event.duracion,
            event.rutaImagen,
            event.tipoClasificado.value if event.tipoClasificado else None,
            event.tipoReal.value if event.tipoReal else None,
            event.admin_id,
            event.confianza
        )

        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
            conn.commit()
        finally:
            conn.close()

    # ------------------------
    # 🔵 Consultar todos los eventos
    # ------------------------
    def get_all_events(self):
        query = "SELECT * FROM Evento ORDER BY horaSincronizado DESC;"
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return [EventModel.from_dict(row) for row in results]
        finally:
            conn.close()

    # ------------------------
    # 🟡 Obtener eventos paginados
    # ------------------------
    def get_paginated_events(self, page: int = 1, page_size: int = 10):
        """Obtiene eventos paginados, con total de registros."""
        page = max(1, int(page))
        page_size = min(max(1, int(page_size)), 100)

        offset = (page - 1) * page_size

        query = """
            SELECT SQL_CALC_FOUND_ROWS *
            FROM Evento
            ORDER BY horaSincronizado DESC
            LIMIT %s OFFSET %s;
        """

        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (page_size, offset))
                results = cursor.fetchall()

                # Obtener total de registros
                cursor.execute("SELECT FOUND_ROWS();")
                total = cursor.fetchone()["FOUND_ROWS()"]

                eventos = [EventModel.from_dict(row) for row in results]

            return {
                "page": page,
                "page_size": page_size,
                "total": total,
                "events": [e.to_dict() for e in eventos]
            }
        finally:
            conn.close()


    # 🟣 Obtener un evento por ID
    # ------------------------
    def get_event_by_id(self, event_id: int):
        query = "SELECT * FROM Evento WHERE id = %s;"
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (event_id,))
                row = cursor.fetchone()
                return EventModel.from_dict(row) if row else None
        finally:
            conn.close()

    # ------------------------
    # 🟠 Actualizar tipoReal
    # ------------------------
    def update_event(self, event_id: int, tipo_real=None):
        query = "UPDATE Evento SET tipoReal = %s WHERE id = %s;"
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (tipo_real, event_id))
            conn.commit()
            return True
        finally:
            conn.close()

    # ------------------------
    # 🔴 Eliminar un evento
    # ------------------------
    def delete_event(self, event_id: int):
        query = "DELETE FROM Evento WHERE id = %s;"
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (event_id,))
            conn.commit()
            return True
        finally:
            conn.close()
