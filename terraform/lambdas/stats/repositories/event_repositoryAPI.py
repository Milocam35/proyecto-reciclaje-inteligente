import requests
import os

class EventRepositoryAPI:
    """
    Repositorio que consume la API de eventos (lambda events) a través de API Gateway.
    """

    def __init__(self):
        # URL base de la API de eventos (puedes pasarla como variable de entorno en Terraform)
        self.base_url = os.getenv("EVENT_API_URL", "https://rdn6x8ojtd.execute-api.us-east-1.amazonaws.com")

    def get_all_events(self):
        """
        Llama al endpoint GET /events para obtener todos los eventos.
        """
        url = f"{self.base_url}/events"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
