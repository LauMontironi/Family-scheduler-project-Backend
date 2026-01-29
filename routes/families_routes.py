from fastapi import APIRouter, Depends
from controller import families_controller
from core.dependencies import get_current_user, require_family_admin, require_family_member
from models.families_model import CreateFamily, UpdateFamily

router = APIRouter()

# Mis familias (donde soy miembro)
@router.get('/my', status_code=200)
async def get_my_families(current_user = Depends(get_current_user)):
    return await families_controller.get_my_families(current_user["id"])

# Crear una familia nueva
@router.post('/', status_code=201)
async def create_family(payload: CreateFamily, current_user = Depends(get_current_user)):
    return await families_controller.create_family(payload, current_user["id"])

# Obtener una familia por ID (solo si eres miembro)
@router.get('/{family_id}', status_code=200)
async def get_family_by_id(family_id: int, m = Depends(require_family_member)):
    return await families_controller.get_family_by_id(family_id)

# Actualizar nombre de familia (solo admin)
@router.put('/{family_id}', status_code=200)
async def update_family(family_id: int, payload: UpdateFamily, m = Depends(require_family_admin)):
    return await families_controller.update_family(family_id, payload)

# Eliminar familia (solo admin)
@router.delete('/{family_id}', status_code=200)
async def delete_family(family_id: int, m = Depends(require_family_admin)):
    return await families_controller.delete_family(family_id)
