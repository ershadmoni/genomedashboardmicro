from fastapi import APIRouter

from app.schemas.sequence import SequenceRequest
from app.services.sequence_service import SequenceService

router = APIRouter()


@router.post("/steps")
def get_steps(request: SequenceRequest):

    steps = SequenceService.get_steps(
        request.sequence
    )

    return {
        "steps": steps
    }
