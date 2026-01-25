from fastapi import HTTPException 
import aiomysql as aio
from db.config import get_conexion
from models.children_model import CreateChild, modifyChild

"""Verificar que la family exista"""

async def family_exists(family_id: int) -> bool:
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT id FROM family_schedule.families WHERE id=%s",
                (family_id,)
            )
            fam = await cursor.fetchone()
            if not fam:
                raise HTTPException(status_code=404, detail="Family no existe")
            return True
    finally:
            conn.close()


"""GET children por familia"""


async def get_children_by_family(family_id: int):
    try:
        await family_exists(family_id)
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM family_schedule.children WHERE family_id=%s",
                (family_id,)
            )
            children= await cursor.fetchall()
            return children
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


"""GET child por id dentro de familia"""

async def get_child_by_id_in_family(family_id: int, id_children: int):
    try:
        await family_exists(family_id)
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM family_schedule.children WHERE id=%s AND family_id=%s",
                (id_children, family_id)
            )
            child = await cursor.fetchone()
            if not child:
                raise HTTPException(status_code=404, detail="Child no existe en esta familia")
            return child
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()



"""POST create child"""


async def create_new_child(family_id: int, child: CreateChild):
   
    try:
        await family_exists(family_id)

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                INSERT INTO family_schedule.children (family_id, name, birthdate, notes)
                VALUES (%s, %s, %s, %s)
                """,
                (family_id, child.name, child.birthdate, child.notes)
            )
            await conn.commit()

            new_id = cursor.lastrowid

        created = await get_child_by_id_in_family(family_id, new_id)
        return {"msg": "Child successfully registered", "item": created}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    finally:
    
            conn.close()

"""Update children in family"""
async def update_child(family_id:int, id_children:int, child:modifyChild):
    try:    
        ok_to_modify = await family_exists(family_id)
        child_exist = await get_child_by_id_in_family(family_id, id_children)

        if child.id != id_children:
            raise HTTPException(status_code=400, detail = 'el id introducido no coincide con el id que desea modificar')
        
            
        if ok_to_modify and child_exist is not None:
            
                conn = await get_conexion()
                async with conn.cursor (aio.DictCursor) as cursor:
                    await cursor.execute ('UPDATE  family_schedule.children SET name=%s, birthdate= %s, notes=%s WHERE id=%s AND family_id=%s',(
                        child.name,
                        child.birthdate,
                        child.notes,
                        id_children,
                        family_id
                    ) )
                    await conn.commit()
                    child_updated=await get_child_by_id_in_family(family_id, id_children)

                    return {'msg': f'Children {child.name} has been succesfully updated', 'item': child_updated}
        raise HTTPException (status_code= 409, detail = ' el id_familia o el id_children son oncorrectos ') 
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()
        
async def delete_children(family_id:int, id_children:int):
    conn = None
    try:    
        ok_to_delete = await family_exists(family_id)
        child_exist = await get_child_by_id_in_family(family_id, id_children)

        if ok_to_delete and child_exist is not None:

                conn = await get_conexion()
                async with conn.cursor (aio.DictCursor) as cursor:
                    await cursor.execute ('DELETE FROM family_schedule.children WHERE id = %s AND family_id = %s',(id_children, family_id) )
                    await conn.commit()

                    return {'msg': f'Children  has been succesfully eliminated'}
        raise HTTPException(status_code=409, detail="el id_familia o el id_children son incorrectos")        
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()