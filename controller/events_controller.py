from fastapi import HTTPException
import aiomysql as aio
from db.config import get_conexion
from models.event_model import EventCreate, EventUpdate

def validate_event_dates(start_at, end_at):
    if end_at is not None and end_at < start_at:
        raise HTTPException(status_code=400, detail="end_at no puede ser menor que start_at")

async def family_exists(family_id: int):
    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT id FROM families WHERE id=%s", (family_id,))
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Family no existe")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

async def member_exists_in_family(family_id: int, member_id: int):
    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT id FROM members WHERE id=%s AND family_id=%s",
                (member_id, family_id)
            )
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="El miembro no existe en esta familia")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

async def get_event_by_id_in_family(family_id: int, event_id: int):
    await family_exists(family_id)
    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM events WHERE id=%s AND family_id=%s",
                (event_id, family_id)
            )
            event = await cursor.fetchone()
            if not event:
                raise HTTPException(status_code=404, detail="Event no existe en esta familia")
            return event
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

async def create_new_event(family_id: int, member_id: int, event: EventCreate):
    await family_exists(family_id)
    await member_exists_in_family(family_id, member_id)
    validate_event_dates(event.start_at, event.end_at)

    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                INSERT INTO events
                (family_id, member_id, title, type, start_at, end_at, location, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                family_id,
                member_id,
                event.title,
                event.type,
                event.start_at,
                event.end_at,
                event.location,
                event.description
            ))
            await conn.commit()
            new_id = cursor.lastrowid

        return await get_event_by_id_in_family(family_id, new_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

async def get_events_by_family(family_id: int):
    await family_exists(family_id)
    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM events WHERE family_id=%s ORDER BY start_at",
                (family_id,)
            )
            return await cursor.fetchall()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

async def update_event(family_id: int, event_id: int, event: EventUpdate):
    await family_exists(family_id)
    await get_event_by_id_in_family(family_id, event_id)
    validate_event_dates(event.start_at, event.end_at)

    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                UPDATE events
                SET title=%s, type=%s, start_at=%s, end_at=%s, location=%s, description=%s
                WHERE id=%s AND family_id=%s
            """, (
                event.title,
                event.type,
                event.start_at,
                event.end_at,
                event.location,
                event.description,
                event_id,
                family_id
            ))
            await conn.commit()

        return await get_event_by_id_in_family(family_id, event_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

async def delete_event(family_id: int, event_id: int):
    await family_exists(family_id)
    await get_event_by_id_in_family(family_id, event_id)

    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "DELETE FROM events WHERE id=%s AND family_id=%s",
                (event_id, family_id)
            )
            await conn.commit()
        return {"msg": "Event eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

async def get_events_by_member(family_id: int, member_id: int):
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT
                    id,
                    family_id,
                    member_id,
                    title,
                    description,
                    location,
                    `type`,
                    start_at,
                    end_at
                FROM events
                WHERE family_id = %s AND member_id = %s
                ORDER BY start_at ASC
                """,
                (family_id, member_id)
            )

            events = await cursor.fetchall()

            if events:
                return events

            raise HTTPException(status_code=404, detail="No hay eventos para este miembro en esta familia.")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()
            try:
                await conn.wait_closed()
            except Exception:
                pass