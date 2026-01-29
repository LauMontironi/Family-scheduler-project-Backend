from fastapi import APIRouter, Depends
from controller import fmembers_controller
from core.dependencies import get_current_user
from models.fmembers_model import MemberCreate, UpdateFamilyMember

router = APIRouter()

@router.get('/summary/all')
async def get_dashboard(u=Depends(get_current_user)):
    return await fmembers_controller.get_dashboard(u["family_id"])

@router.get('/families/{family_id}')
async def get_members(family_id: int):
    return await fmembers_controller.get_members_by_family(family_id)

@router.post('/')
async def create(payload: MemberCreate, u=Depends(get_current_user)):
    return await fmembers_controller.create_member(u["family_id"], payload)

@router.put('/{member_id}')
async def update(member_id: int, payload: UpdateFamilyMember, u=Depends(get_current_user)):
    return await fmembers_controller.update_member_profile(u["family_id"], member_id, payload)

@router.delete('/{member_id}')
async def delete(member_id: int, u=Depends(get_current_user)):
    return await fmembers_controller.delete_member(u["family_id"], member_id)