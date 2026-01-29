from fastapi import HTTPException, Depends, Path
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_token
from controller.auth_controller import get_user_by_id
from db.config import get_conexion
import aiomysql as aio

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token sin id")

    user = await get_user_by_id(int(user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    return user



async def is_owner(
    user=Depends(get_current_user),
    user_id_path: int = Path(...)
):
    if user["id"] == user_id_path:
        return user
    raise HTTPException(status_code=403, detail="No tienes permiso")




async def require_family_member(family_id: int = Path(...),
    user=Depends(get_current_user)
):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT relationship
                FROM members
                WHERE family_id=%s AND id=%s
                """,
                (family_id, user["id"])
            )
            membership = await cursor.fetchone()
            if membership is None:
                raise HTTPException(status_code=403, detail="No perteneces a esta familia")

            # devolvemos info útil por si luego quieres validar admin
            return {
                "user": user,
                "role": membership["relationship"]
            }
    finally:
        conn.close()


#  Admin-only: require_family_admin  solo admin pueda update/delete family:

async def require_family_admin(m=Depends(require_family_member)):
    if m["role"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede realizar esta acción")
    return m