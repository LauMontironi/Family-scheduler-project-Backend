from fastapi import HTTPException
import aiomysql as aio
from db.config import get_conexion
from controller.children_controller import family_exists
from models.fmembers_model import UpdateFamilyMember


# GET members by family
async def get_members_by_family(family_id: int):
    try:
        await family_exists(family_id)

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT
                    fm.id AS family_member_id,
                    fm.family_id,
                    fm.user_id,
                    u.full_name,
                    u.email,
                    fm.role,
                    fm.relationship_label,
                    fm.avatar_url,
                    fm.created_at
                FROM family_schedule.family_members fm
                JOIN family_schedule.users u ON u.id = fm.user_id
                WHERE fm.family_id = %s
                ORDER BY fm.created_at
                """,
                (family_id,)
            )
            members = await cursor.fetchall()
            return members

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# PUT member profile (relationship_label, avatar_url)
async def update_member_profile(family_id: int, user_id: int, payload: UpdateFamilyMember):
    try:
        await family_exists(family_id)

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # comprobar que ese user es miembro de esa familia
            await cursor.execute(
                """
                SELECT id FROM family_schedule.family_members
                WHERE family_id=%s AND user_id=%s
                """,
                (family_id, user_id)
            )
            fm = await cursor.fetchone()
            if fm is None:
                raise HTTPException(status_code=404, detail="Ese usuario no es miembro de esta familia")

            # update simple (tu estilo PUT completo para esos 2 campos)
            await cursor.execute(
                """
                UPDATE family_schedule.family_members
                SET relationship_label=%s, avatar_url=%s
                WHERE family_id=%s AND user_id=%s
                """,
                (payload.relationship_label, payload.avatar_url, family_id, user_id)
            )
            await conn.commit()

            # devolver el miembro actualizado (con JOIN para que salga full_name)
            await cursor.execute(
                """
                SELECT
                    fm.id AS family_member_id,
                    fm.family_id,
                    fm.user_id,
                    u.full_name,
                    u.email,
                    fm.role,
                    fm.relationship_label,
                    fm.avatar_url,
                    fm.created_at
                FROM family_schedule.family_members fm
                JOIN family_schedule.users u ON u.id = fm.user_id
                WHERE fm.family_id = %s AND fm.user_id = %s
                """,
                (family_id, user_id)
            )
            updated = await cursor.fetchone()

            return {"msg": "Family member profile updated", "item": updated}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()
