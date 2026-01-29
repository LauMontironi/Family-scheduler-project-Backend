from fastapi import APIRouter, Depends
from controller import auth_controller
from core.dependencies import get_current_user
from models.user_model import UserCreate, User, UserLogin


## RUTAS DE AUTENICADO :

router= APIRouter()

@router.get("/me", status_code=200)
async def me(current_user=Depends(get_current_user)):
    return current_user


@router.get('/users/{user_id}', status_code=200)
async def get_user(
    user_id: str, current_user=Depends(get_current_user)
):
    return await auth_controller.get_user_by_id(int(user_id))

@router.post('/register', status_code=201)
async def register(user: UserCreate):
    return await auth_controller.register_new_user(user)

@router.post('/login', status_code=200)
async def login(payload: UserLogin):
    return await auth_controller.login_user(payload)

