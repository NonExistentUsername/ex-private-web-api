from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas.user
import schemas.command
import models.user
import crud.user
import crud.command
import crud.app
import core.deps
from starlette.responses import FileResponse

from fastapi_pagination import Page, paginate

router = APIRouter()


@router.post("/auth/register/", response_model=schemas.user.User, status_code=201)
async def create_user(user: schemas.user.UserCreate, db: Session = Depends(core.deps.get_db)):
    return crud.user.register_user(user, db)


@router.post("/auth/login/")
async def login(user: schemas.user.UserLogin, db: Session = Depends(core.deps.get_db)):
    return crud.user.login_user(user, db)


@router.get("/auth/me", response_model=schemas.user.User)
async def read_users_me(current_user: models.user.User = Depends(core.deps.get_current_user)):
    user = current_user
    return user


@router.get("/users/", response_model=Page[schemas.user.User])
async def get_users(db: Session = Depends(core.deps.get_db), current_user: models.user.User = Depends(core.deps.get_current_user)):
    return paginate(crud.user.get_users(db, current_user))


@router.post("/users/update_rights/", response_model=schemas.user.User)
async def update_rights(is_admin: bool, nickname: str, db: Session = Depends(core.deps.get_db), current_user: models.user.User = Depends(core.deps.get_current_user)):
    return crud.user.set_admin_rights_for_user(is_admin, nickname, db, current_user)


@router.get("/app/commands", response_model=Page[schemas.command.Command])
async def get_commands(db: Session = Depends(core.deps.get_db), current_user: models.user.User = Depends(core.deps.get_current_user)):
    return paginate(crud.command.get_commands(db, current_user))


@router.post("/app/send_command", response_model=schemas.command.Command)
async def send_command(command: schemas.command.CommandCreate, db: Session = Depends(core.deps.get_db), current_user: models.user.User = Depends(core.deps.get_current_user)):
    return crud.command.send_command(command, db, current_user)


@router.get("/app/last_update")
async def get_last_app_update(current_user: models.user.User = Depends(core.deps.get_current_user)):
    return crud.app.get_last_app_update(current_user)


@router.get("/app/download", response_class=FileResponse)
async def get_last_app_update(current_user: models.user.User = Depends(core.deps.get_current_user)):
    return crud.app.download_app(current_user)