import pymysql
import os
from models.error_model import ErrorModel
class ErrorRepository:
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
    # Crear un nuevo error
    # ------------------------
    def insert_error(self, error: ErrorModel):
        query = """
        INSERT INTO Error (
            hora, fuente, mensaje, event_id
        ) VALUES (%s, %s, %s, %s);
        """
        values = (
            error.hora.strftime("%Y-%m-%d %H:%M:%S"),
            error.fuente,
            error.mensaje,
            error.event_id
        )

        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
            conn.commit()
        finally:
            conn.close()

    # ------------------------
    # Consultar todos los errores
    # ------------------------
    def get_all_errors(self):
        query = "SELECT id, hora, fuente, mensaje, event_id FROM Error;"
        
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                errors = [ErrorModel.from_dict(row) for row in results]
                return errors
        finally:
            conn.close()
    
    # ------------------------
    # Consultar errores por event_id
    # ------------------------
    def get_errors_by_event_id(self, event_id):
        query = "SELECT id, hora, fuente, mensaje, event_id FROM Error WHERE event_id = %s;"
        
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (event_id,))
                results = cursor.fetchall()
                errors = [ErrorModel.from_dict(row) for row in results]
                return errors
        finally:
            conn.close()
    
    # ------------------------
    # Eliminar errores por event_id
    # ------------------------
    def delete_errors_by_event_id(self, event_id):
        query = "DELETE FROM Error WHERE event_id = %s;"
        
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (event_id,))
            conn.commit()
        finally:
            conn.close()