from pydantic import BaseModel, Field, validator
from typing import List


class EnergyRequest(BaseModel):
    """
    Request schema for single energy computation.
    """

    vector: List[float] = Field(
        ...,
        description="Deformation vector (length 6)"
    )

    stiffness: List[List[float]] = Field(
        ...,
        description="6x6 stiffness matrix"
    )

    @validator("vector")
    def validate_vector(cls, v):
        if len(v) != 6:
            raise ValueError("Vector must have length 6")
        return v

    @validator("stiffness")
    def validate_stiffness(cls, v):
        if len(v) != 6 or any(len(row) != 6 for row in v):
            raise ValueError("Stiffness matrix must be 6x6")
        return v


class EnergyResponse(BaseModel):
    """
    Response schema for single energy.
    """
    energy: float


class EnergyProfileRequest(BaseModel):
    """
    Request schema for batch energy computation.
    """

    vectors: List[List[float]] = Field(
        ...,
        description="List of deformation vectors"
    )

    stiffness: List[List[float]]

    @validator("vectors")
    def validate_vectors(cls, v):
        for vec in v:
            if len(vec) != 6:
                raise ValueError("Each vector must have length 6")
        return v


class EnergyProfileResponse(BaseModel):
    """
    Response schema for energy profile.
    """
    energies: List[float]
