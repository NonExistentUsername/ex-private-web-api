from fastapi import APIRouter, Depends, WebSocket
import models.user
import crud.user
import crud.command
import crud.app
import core.deps
import core.global_variables

commands_ws_router = APIRouter()


@commands_ws_router.websocket("/get_commands")
async def ws_get_updates(websocket: WebSocket, current_user: models.user.User = Depends(core.deps.get_current_user_from_websocket)):
    await crud.command.ws_get_commands(websocket, current_user)
