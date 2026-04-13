from fastapi import APIRouter

from app.schemas.geometry import HPRequest
from app.services.geometry_service import GeometryService

router = APIRouter()


@router.post("/build")
def build_structure(request: HPRequest):

    structure = GeometryService.build_structure(
        request.hp_list
    )

    return {
        "structure": structure
    }
