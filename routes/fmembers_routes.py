from fastapi import APIRouter
from controller import fmembers_controller
from models.fmembers_model import UpdateFamilyMember

router = APIRouter()

# LISTAR MIEMBROS DE UNA FAMILIA (para cards)
@router.get('/families/{family_id}', status_code=200)
async def get_members_by_family(family_id: str):
    return await fmembers_controller.get_members_by_family(int(family_id))

# UPDATE PERFIL DE MIEMBRO (temporal, luego con JWT será "mi perfil")
@router.put('/families/{family_id}/users/{user_id}', status_code=200)
async def update_member_profile(family_id: str, user_id: str, payload: UpdateFamilyMember):
    return await fmembers_controller.update_member_profile(int(family_id), int(user_id), payload)
