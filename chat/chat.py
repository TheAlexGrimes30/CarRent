from fastapi import WebSocket

from db.orm import SyncOrm

sync_orm = SyncOrm()


class ConnectionManager(object):
    """
    Класс хранит активные websocket соединения
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_email: str):
        await websocket.accept()
        self.active_connections[user_email] = websocket

    def disconnect(self, user_email: str):
        del self.active_connections[user_email]

    async def send_personal_message(self, message: str, websocket: WebSocket,
                                    user_email: str = None):
        if user_email is None:
            await websocket.send_text(message)
        else:
            await self.active_connections[user_email].send_text(message)

    async def send_admin_message(self, message: str, user_email: str):
        if 'admin' in self.active_connections:
            json = {
                'message': message,
                'user_email': user_email
            }
            await self.active_connections['admin'].send_json(json)


manager = ConnectionManager()



