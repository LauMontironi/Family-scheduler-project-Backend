from fastapi import HTTPException 
import aiomysql as aio
from core.security import create_token, hash_password, verify_password
from db.config import get_conexion
from models.auth_model import UserCreate
from models.user_model import UserLogin




async def get_user_by_id(user_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT id, email, full_name, family_id, is_admin 
                FROM members 
                WHERE id=%s
                """, 
                (user_id,)
            )
            user = await cursor.fetchone()
            if user is None:
                raise HTTPException(status_code=404, detail="Usuario no existe")
            return user

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()




async def register_new_user(user:UserCreate):
    existing = await get_user_by_email(user.email)
    if existing: raise HTTPException(status_code=400, detail="Email ya registrado")
    try:
        conn= await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # aca se hasea al password tengo que importar la funcion hash que hice el security
            hashed_pass = hash_password(user.password)
            await cursor.execute(
                'INSERT INTO members (email, password, full_name) VALUES (%s,%s,%s)', (
                    user.email, 
                    hashed_pass, 
                    user.full_name 
                    ))
            await conn.commit()
            new_id= cursor.lastrowid
            user = await get_user_by_id(new_id)
            return {'msg': 'usuario registrado correctamente', 'item': user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


async def get_user_by_email(email: str):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT id, email, password, full_name FROM members WHERE email=%s",
                (email,)
            )
            user = await cursor.fetchone()
            return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


async def login_user(payload: UserLogin):
    try:
        user = await get_user_by_email(payload.email)

     
        if user is None:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        if not verify_password(payload.password, user["password"]):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        token_data = {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"]
        }

        token=create_token(token_data)

        return {
            "msg": "Login correcto",
            "Token":token,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
                "family_id": user.get("family_id")
               
                
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    


async def register_new_user(user: UserCreate):
   
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            hashed_pass = hash_password(user.password)
            #
            await cursor.execute(
                'INSERT INTO members (email, password, full_name) VALUES (%s,%s,%s)', 
                (user.email, hashed_pass, user.full_name)
            )
            await conn.commit()
            new_id = cursor.lastrowid
            return await get_user_by_id(new_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()
