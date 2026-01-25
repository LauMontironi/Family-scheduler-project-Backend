from fastapi import HTTPException
import aiomysql as aio
from controller.children_controller import family_exists, get_child_by_id_in_family
from db.config import get_conexion
from models.event_model import EventCreate, EventUpdate
from datetime import datetime

def validate_event_dates(start_at, end_at):
    if end_at is not None and end_at < start_at:
        raise HTTPException(status_code=400, detail="end_at no puede ser menor que start_at")


# get event by id (dentro de family)
async def get_event_by_id_in_family(family_id: int, event_id: int):
    try:
        await family_exists(family_id)

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM family_schedule.events WHERE id=%s AND family_id=%s",
                (event_id, family_id)
            )
            event = await cursor.fetchone()
            if not event:
                raise HTTPException(status_code=404, detail="Event no existe en esta familia")
            return event

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# create event
async def create_new_event(family_id: int, child_id: int, event: EventCreate):
    try:
        await family_exists(family_id)
        await get_child_by_id_in_family(family_id, child_id)
        validate_event_dates(event.start_at, event.end_at)

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                INSERT INTO family_schedule.events
                (family_id, child_id, created_by, title, type, start_at, end_at, location, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    family_id,
                    child_id,
                    event.created_by,
                    event.title,
                    event.type.value,
                    event.start_at,
                    event.end_at,
                    event.location,
                    event.notes
                )
            )
            await conn.commit()
            new_id = cursor.lastrowid

        new_event = await get_event_by_id_in_family(family_id, new_id)
        return {"msg": "New event successfully registered", "item": new_event}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


# get events by family (list)
async def get_events_by_family(family_id: int):
    try:
        await family_exists(family_id)

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM family_schedule.events WHERE family_id=%s ORDER BY start_at",
                (family_id,)
            )
            events = await cursor.fetchall()
            return events

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# update
async def update_event(family_id: int, event_id: int, event: EventUpdate):
    conn = None
    try:
        await family_exists(family_id)

        if event.id != event_id:
            raise HTTPException(status_code=400, detail="El id del body no coincide con el event_id de la ruta")

        await get_event_by_id_in_family(family_id, event_id)

        validate_event_dates(event.start_at, event.end_at)

        if event.child_id is not None:
            await get_child_by_id_in_family(family_id, event.child_id)

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                UPDATE family_schedule.events
                SET child_id=%s, created_by=%s, title=%s, type=%s,
                    start_at=%s, end_at=%s, location=%s, notes=%s
                WHERE id=%s AND family_id=%s
                """,
                (
                    event.child_id,
                    event.created_by,
                    event.title,
                    event.type.value,
                    event.start_at,
                    event.end_at,
                    event.location,
                    event.notes,
                    event_id,
                    family_id
                )
            )
            await conn.commit()

        updated = await get_event_by_id_in_family(family_id, event_id)
        return {"msg": f"Event {event.title} has been successfully updated", "item": updated}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


# delete
async def delete_event(family_id: int, event_id: int):
    try:
        await family_exists(family_id)
        await get_event_by_id_in_family(family_id, event_id)

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "DELETE FROM family_schedule.events WHERE id=%s AND family_id=%s",
                (event_id, family_id)
            )
            await conn.commit()

        return {"msg": "Event has been successfully deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

#########FILTROS ############POR TIPO DE EVENTO 
async def get_events_by_type(family_id: int, event_type: str):
    try:
        await family_exists(family_id)

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT * FROM family_schedule.events
                WHERE family_id=%s AND type=%s
                ORDER BY start_at
                """,
                (family_id, event_type)
            )
            events = await cursor.fetchall()
            return events

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


#########FILTROS ############POR HIJO
async def get_events_by_child(family_id: int, child_id: int):
    try:
        await family_exists(family_id)
        await get_child_by_id_in_family(family_id, child_id)

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT * FROM family_schedule.events
                WHERE family_id=%s AND child_id=%s
                ORDER BY start_at
                """,
                (family_id, child_id)
            )
            events = await cursor.fetchall()
            return events

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


#########FILTROS ############POR RAGO DE FECHA 


async def get_events_by_date_range(family_id: int, start: str, end: str):
    try:
        await family_exists(family_id)

        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT * FROM family_schedule.events
                WHERE family_id=%s
                AND start_at BETWEEN %s AND %s
                ORDER BY start_at
                """,
                (family_id, start_dt, end_dt)
            )
            return await cursor.fetchall()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()
