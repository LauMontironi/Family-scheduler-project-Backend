from fastapi import APIRouter, Depends
from controller import fmembers_controller
from core.dependencies import get_current_user
from models.fmembers_model import UpdateFamilyMember
from models.user_model import User

router = APIRouter()


@router.get('/summary/all', status_code=200)
async def get_dashboard(current_user: User = Depends(get_current_user)):
    family_id = current_user.family_id 
    return await fmembers_controller.get_dashboard(family_id)





# LISTAR MIEMBROS DE UNA FAMILIA (para cards)
@router.get('/families/{family_id}', status_code=200)
async def get_members_by_family(family_id: str):
    return await fmembers_controller.get_members_by_family(int(family_id))




# UPDATE PERFIL DE MIEMBRO (temporal, luego con JWT será "mi perfil")
@router.put('/families/{family_id}/users/{user_id}', status_code=200)
async def update_member_profile(family_id: str, user_id: str, payload: UpdateFamilyMember):
    return await fmembers_controller.update_member_profile(int(family_id), int(user_id), payload)


