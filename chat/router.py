from typing import Dict, Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.logger_file import logger
from db.orm import AsyncOrm

chat_router = APIRouter(
    prefix='/chat',
    tags=['chat']
)


class ConnectionManager(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'active_connections'):
            self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        del self.active_connections[user_id]

    async def send_personal_message(self, user_id: int, message: str):
        try:
            admin_ids = await async_orm.get_all_admins()
            if user_id in admin_ids:
                await self.active_connections[user_id].send_text(message)
        except KeyError:
            print(f"User {user_id} is not connected.")
        except Exception as e:
            print(f"Error sending personal message: {e}")

    async def send_admin_message(self, user_id: int, message: str):
        try:
            admin_ids = await async_orm.get_all_admins()
            if user_id not in admin_ids:
                json = {
                    'message': message,
                    'user_id': user_id
                }
                await self.active_connections[user_id].send_json(json)
        except KeyError:
            print(f"User {user_id} is not connected.")

        except Exception as e:
            print(f"Error sending personal message: {e}")

    @staticmethod
    async def add_messages_to_database(user_id: int, message: str):
        await async_orm.insert_message_to_db(user_id, message)


manager = ConnectionManager()
async_orm = AsyncOrm()


@chat_router.websocket('/ws/{user_id}')
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    logger.info(f"User {user_id} connected the chat")
    try:
        while True:
            data = await websocket.receive_json()
            message = data['message']
            if async_orm.get_user_role(user_id):
                await manager.send_personal_message(user_id, message)
            else:
                await manager.send_admin_message(user_id, message)
            await manager.add_messages_to_database(user_id, message)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        logger.info(f"User {user_id} has left the chat")


@chat_router.get('/messages/{user_id}')
async def get_user_messages(user_id: int, limit: Optional[int] = None, offset: Optional[int] = None):
    result = await async_orm.get_user_messages(user_id, limit, offset)
    logger.info(f"User messages with {user_id}")
    return {
        'data': result,
        'status': 'ok'
    }
