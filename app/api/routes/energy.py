from fastapi import APIRouter, HTTPException

from app.schemas.energy import (
    EnergyRequest,
    EnergyResponse,
    EnergyProfileRequest,
    EnergyProfileResponse
)
from app.services.energy_service import EnergyService

import numpy as np


router = APIRouter()


@router.post("/compute", response_model=EnergyResponse)
def compute_energy(request: EnergyRequest):
    """
    Compute elastic energy for a single deformation vector.
    """
    try:
        vector = np.array(request.vector)
        stiffness = np.array(request.stiffness)

        energy = EnergyService.compute_energy(vector, stiffness)

        return EnergyResponse(energy=energy)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Energy computation failed: {str(e)}"
        )


@router.post("/profile", response_model=EnergyProfileResponse)
def compute_energy_profile(request: EnergyProfileRequest):
    """
    Compute energy over multiple deformation vectors.
    """
    try:
        stiffness = np.array(request.stiffness)

        energies = []

        for vec in request.vectors:
            vector = np.array(vec)
            energy = EnergyService.compute_energy(vector, stiffness)
            energies.append(energy)

        return EnergyProfileResponse(energies=energies)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Energy profile computation failed: {str(e)}"
        )
