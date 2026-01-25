from fastapi import APIRouter
from controller import events_controller
from models.event_model import EventCreate, EventUpdate


router = APIRouter()

### CREATE EVENT 

@router.post('/families/{family_id}/children/{child_id}/events', status_code=201)
async def create_new_event(family_id: str, child_id: str, event: EventCreate):
    return await events_controller.create_new_event(int(family_id), int(child_id), event)

# get events by family (list)

@router.get('/families/{family_id}', status_code=200)
async def get_events_by_family(family_id: str):
    return await events_controller.get_events_by_family(int(family_id))


# get event by id (dentro de family)

@router.get('/families/{family_id}/events/{event_id}', status_code=200)
async def get_event_by_id(family_id: str, event_id: str):
    return await events_controller.get_event_by_id_in_family(int(family_id), int(event_id))

##update

@router.put('/families/{family_id}/events/{event_id}', status_code=200)
async def update_event(family_id: str, event_id: str, event: EventUpdate):
    return await events_controller.update_event(int(family_id), int(event_id), event)

###DELETE 

@router.delete('/families/{family_id}/events/{event_id}', status_code=200)
async def delete_event(family_id: str, event_id: str):
    return await events_controller.delete_event(int(family_id), int(event_id))


##  FILTROS 
@router.get('/families/{family_id}/events/type/{event_type}', status_code=200)
async def get_events_by_type(family_id: str, event_type: str):
    return await events_controller.get_events_by_type(int(family_id), event_type)

@router.get('/families/{family_id}/children/{child_id}/events', status_code=200)
async def get_events_by_child(family_id: str, child_id: str):
    return await events_controller.get_events_by_child(int(family_id), int(child_id))


@router.get('/families/{family_id}/events/range', status_code=200)
async def get_events_by_date_range(family_id: str, start: str,end: str
):
    return await events_controller.get_events_by_date_range(
        int(family_id), start, end
    )
