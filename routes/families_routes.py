from fastapi import APIRouter, Depends
from controller import families_controller
from core.dependencies import get_current_user, require_family_admin, require_family_member
from models.families_model import CreateFamily ,UpdateFamily



router= APIRouter()

@router.get('/my', status_code=200)
async def get_my_families(current_user=Depends(get_current_user)):
    return await families_controller.get_my_families(current_user["id"])

# LISTADO: normalmente NO debe devolver todas las families del sistema.
# Lo ideal: "mis familias" (lo hacemos luego). Por ahora, protégelo al menos con token.
@router.get('/', status_code=200)
async def get_all_families(current_user=Depends(get_current_user)):
    return await families_controller.get_all_families()


# GET family by id: requiere pertenencia
@router.get('/{family_id}', status_code=200)
async def get_family_by_id(family_id: str, m=Depends(require_family_member)):
    return await families_controller.get_family_by_id(int(family_id))


# CREATE family: requiere token
@router.post('/', status_code=201)
async def create_family(family: CreateFamily, current_user=Depends(get_current_user)):
    return await families_controller.create_family(family, current_user["id"])


# UPDATE family: admin-only
@router.put('/{family_id}', status_code=200)
async def update_family(family_id: str, family: UpdateFamily, m=Depends(require_family_admin)):
    return await families_controller.update_family(int(family_id), family)


# DELETE family: admin-only
@router.delete('/{family_id}', status_code=200)
async def delete_family(family_id: str, m=Depends(require_family_admin)):
    return await families_controller.delete_family(int(family_id))


