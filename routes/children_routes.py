from fastapi import APIRouter
from controller import children_controller
from models.children_model import CreateChild, modifyChild  

router = APIRouter()

@router.get('/families/{family_id}/children', status_code=200)
async def get_children_by_family(family_id: str):
    return await children_controller.get_children_by_family(int(family_id))

@router.get('/families/{family_id}/children/{id_children}', status_code=200)
async def get_child_by_id(family_id: str, id_children: str):
    return await children_controller.get_child_by_id_in_family(int(family_id), int(id_children))

@router.post('/families/{family_id}/children', status_code=201)
async def create_new_child(family_id: str, child: CreateChild):
    return await children_controller.create_new_child(int(family_id), child)

@router.put('/families/{family_id}/children/{id_children}', status_code=200)
async def update_child(family_id:str, id_children:str, child:modifyChild):
    return await children_controller.update_child(int(family_id), int(id_children), child)

@router.delete('/families/{family_id}/children/{id_children}', status_code=200)
async def delete_children(family_id:str, id_children:str):
    return await children_controller.delete_children(int(family_id), int(id_children))