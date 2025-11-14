from enum import Enum

class NotificationType(Enum):
    INFO = "info"
    SUCCESS = "success"
    ERROR = "error"

class NotificationDTO:
    def __init__(self, id: str = None, message: str = None, recipient: str = None, timestamp: str = None, type: NotificationType = None):
        self.id = id
        self.message = message
        self.recipient = recipient
        self.timestamp = timestamp
        self.type = type

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "message": self.message,
            "recipient": self.recipient,
            "timestamp": self.timestamp,
        }