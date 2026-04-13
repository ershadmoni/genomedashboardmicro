from pydantic import BaseModel


class HPModel(BaseModel):
    shift: float
    slide: float
    rise: float
    tilt: float
    roll: float
    twist: float


class HPRequest(BaseModel):
    hp_list: list[HPModel]
