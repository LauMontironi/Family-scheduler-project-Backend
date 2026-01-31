from fastapi import HTTPException
import aiomysql as aio
from db.config import get_conexion
from models.fmembers_model import UpdateFamilyMember




# PUT member profile (relationship_label, avatar_url)
async def update_member_profile(family_id: int, member_id: int, payload: UpdateFamilyMember):
    try:
      
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # comprobar que ese user es miembro de esa familia
            await cursor.execute(
                """
                SELECT id FROM members WHERE id=%s AND family_id=%s
                """,
                (member_id, family_id)
            )
            exists = await cursor.fetchone()
            if not exists:
                raise HTTPException(status_code=404, detail="Miembro no encontrado en esta familia")

            # update simple (tu estilo PUT completo para esos 2 campos)
            await cursor.execute(
                """
                UPDATE members 
                SET relationship=%s, hobbys=%s, city=%s, gender=%s
                WHERE id=%s AND family_id=%s
                """,
                (payload.relationship, payload.hobbys, payload.city, payload.gender, member_id, family_id)
            )
            await conn.commit()

            # devolver el miembro actualizado (con JOIN para que salga full_name)
            await cursor.execute("SELECT * FROM members WHERE id=%s", (member_id,))
            updated = await cursor.fetchone()
            return {"msg": "Perfil actualizado correctamente", "item": updated}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()



async def create_member(family_id: int, member_data):
    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
            is_child_val = 1 if member_data.is_child else 0
            await cursor.execute("""
                INSERT INTO members 
                (family_id, full_name, relationship, is_child, birthdate, gender, city, hobbys, email) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """,
        
            (
                family_id,
                member_data.full_name,
                member_data.relationship,
                1 if member_data.is_child else 0,
                member_data.birthdate,
                member_data.gender,
                member_data.city,
                member_data.hobbys,
                member_data.email
            ))
           
            await conn.commit()
            return {"msg": "Miembro creado con éxito", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()



async def get_dashboard(family_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # 1. Traemos a TODOS los miembros (Adultos y Niños)
            # En el Front los separarás por 'is_child'
            await cursor.execute('SELECT * FROM members WHERE family_id = %s', (family_id,))
            members = await cursor.fetchall()

            # 2. Traemos todos los eventos
            await cursor.execute('SELECT * FROM events WHERE family_id = %s ORDER BY start_at ASC', (family_id,))
            events = await cursor.fetchall()

            return {
                "members": members,
                "events": events
            }
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        conn.close()

async def delete_member(family_id: int, member_id: int):
    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("DELETE FROM members WHERE id=%s AND family_id=%s", (member_id, family_id))
            await conn.commit()
            return {"msg": "Eliminado"}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        conn.close()

async def get_members_by_family(family_id: int):
    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM members WHERE family_id = %s", (family_id,))
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        conn.close()


async def get_member_by_id(family_id: int, member_id: int):
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM members WHERE id=%s AND family_id=%s",
                (member_id, family_id)
            )
            member = await cursor.fetchone()

            if not member:
                raise HTTPException(status_code=404, detail="Miembro no encontrado en esta familia")

            
            if "password" in member:
                member.pop("password")

            return member

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()
