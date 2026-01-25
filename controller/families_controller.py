from fastapi import HTTPException 
import aiomysql as aio
from db.config import get_conexion
from models.families_model import CreateFamily, UpdateFamily

async def get_all_families():
    try:
        conn= await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute('SELECT * FROM family_schedule.families')
            families = await cursor.fetchall()
            return families
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')
    
    finally:
        conn.close()                   

async def get_family_by_id(id:int):
    try:
        conn= await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute('SELECT * FROM family_schedule.families WHERE id=%s',(id,))
            family = await cursor.fetchone()
            if family is None:
                raise HTTPException(status_code=404 , detail = 'El id introducido no se corresponde con ninguna familia registrada')
            return family
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')
    
    finally:
        conn.close()

async def create_family(family: CreateFamily, user_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "INSERT INTO family_schedule.families (name) VALUES (%s)",
                (family.name,)
            )
            await conn.commit()
            new_family_id = cursor.lastrowid

            # creador = admin de esa family
            await cursor.execute(
                """
                INSERT INTO family_schedule.family_members (family_id, user_id, role)
                VALUES (%s, %s, 'admin')
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
            await cursor.execute('UPDATE family_schedule.families SET name=%s WHERE id =%s',(
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
            await cursor.execute('DELETE  FROM family_schedule.families WHERE id =%s',(id,))
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
            await cursor.execute(
                """
                SELECT
                    f.id AS family_id,
                    f.name AS family_name,
                    f.created_at AS family_created_at,
                    fm.role,
                    fm.relationship_label,
                    fm.avatar_url,
                    fm.created_at AS member_created_at
                FROM family_schedule.family_members fm
                JOIN family_schedule.families f ON f.id = fm.family_id
                WHERE fm.user_id = %s
                ORDER BY f.created_at DESC
                """,
                (user_id,)
            )
            families = await cursor.fetchall()
            return families

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()