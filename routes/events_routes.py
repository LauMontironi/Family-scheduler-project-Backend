from fastapi import APIRouter
from controller import events_controller
from models.event_model import EventCreate, EventUpdate

router = APIRouter()

# Crear evento (asignado a un miembro)
@router.post('/families/{family_id}/members/{member_id}/events', status_code=201)
async def create_new_event(family_id: int, member_id: int, event: EventCreate):
    return await events_controller.create_new_event(family_id, member_id, event)

# Obtener todos los eventos de una familia
@router.get('/families/{family_id}', status_code=200)
async def get_events_by_family(family_id: int):
    return await events_controller.get_events_by_family(family_id)

# Obtener un evento por ID dentro de una familia
@router.get('/families/{family_id}/events/{event_id}', status_code=200)
async def get_event(family_id: int, event_id: int):
    return await events_controller.get_event_by_id_in_family(family_id, event_id)

# Actualizar un evento
@router.put('/families/{family_id}/events/{event_id}', status_code=200)
async def update_event(family_id: int, event_id: int, payload: EventUpdate):
    return await events_controller.update_event(family_id, event_id, payload)

# Eliminar un evento
@router.delete('/families/{family_id}/events/{event_id}', status_code=200)
async def delete_event(family_id: int, event_id: int):
    return await events_controller.delete_event(family_id, event_id)


# Obtener eventos por miembro dentro de una familia
@router.get('/families/{family_id}/members/{member_id}/events', status_code=200)
async def get_events_by_member(family_id: int, member_id: int):
    return await events_controller.get_events_by_member(family_id, member_id)
