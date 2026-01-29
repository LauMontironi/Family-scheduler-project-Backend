from fastapi import HTTPException 
import aiomysql as aio
from db.config import get_conexion
from models.families_model import CreateFamily, UpdateFamily

async def get_all_families():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
           
            await cursor.execute('SELECT * FROM families')
            families = await cursor.fetchall()
            return families
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')
    finally:
        conn.close()                  

async def get_family_by_id(id:int):
    conn = None
    try:
        conn= await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute('SELECT * FROM families WHERE id=%s',(id,))
            family = await cursor.fetchone()
            if family is None:
                raise HTTPException(status_code=404 , detail = 'El id introducido no se corresponde con ninguna familia registrada')
            return family
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')
    
    finally:
        conn.close()

async def create_family(data, user_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # 1. Crear la familia (usando 'family_name' que es lo que pusimos en el SQL)
            await cursor.execute(
                "INSERT INTO families (family_name) VALUES (%s)",
                (data.family_name,)
            )
            await conn.commit()
            new_family_id = cursor.lastrowid

            # 2. El creador se convierte en admin y miembro (usando tabla 'members')
            # Importante: Actualizamos la fila del usuario que acaba de crear la familia
            await cursor.execute(
                """
                UPDATE members 
                SET family_id=%s, is_admin=1, relationship='admin' 
                WHERE id=%s
                """,
                (new_family_id, user_id)
            )
            await conn.commit()

        created = await get_family_by_id(new_family_id)
        return {"msg": "Familia registrada correctamente", "item": created}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


async def update_family(id:int, family:UpdateFamily):
    if id!= family.id:
         raise HTTPException (status_code= 400, detail = 'El id no coincide')
    family_exist = await get_family_by_id(id)
    if family_exist is None:
         raise HTTPException(status_code= 404, detail = 'La familia que desea actualizar no exste')
                              
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute('UPDATE families SET family_name=%s WHERE id =%s',(
                family.name, 
                family.id
            ))
            await conn.commit()
            family=await get_family_by_id(id)
            return {'msg': 'Familia actualizada correctamente', 'item': family}
        
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()

async def delete_family(id:int):

    family_exist =await get_family_by_id(id)
    if family_exist is None:
         raise HTTPException(status_code= 404, detail = 'La familia que desea eliminar no exste')
                              
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute('DELETE FROM families WHERE id =%s', (id,))
            await conn.commit()
            return {'msg': 'Familia eliminada correctamente'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()




async def get_my_families(user_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # SQL simplificado para tu nueva tabla 'members'
            await cursor.execute(
                """
                SELECT f.id AS family_id, f.family_name, f.created_at, m.relationship
                FROM members m
                JOIN families f ON f.id = m.family_id
                WHERE m.id = %s
                """,
                (user_id,)
            )
            families = await cursor.fetchall()
            return families

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()