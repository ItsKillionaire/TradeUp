from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.connection_manager import manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info(f"Attempting to connect WebSocket: {websocket.client}")
    await manager.connect(websocket)
    logger.info(f"WebSocket connected: {websocket.client}")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received message from {websocket.client}: {data}")
            await manager.broadcast(f"Client said: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"WebSocket disconnected: {websocket.client}")
        await manager.broadcast("A client left the chat")
    except Exception as e:
        logger.error(f"WebSocket error for {websocket.client}: {e}")
