from dataclasses import dataclass
from typing import Optional


@dataclass
class HPInter:
    shift: float
    slide: float
    rise: float
    tilt: float
    roll: float
    twist: float


@dataclass
class HPIntra:
    shear: float
    stretch: float
    stagger: float
    buckle: float
    propeller: float
    opening: float


@dataclass
class HelicalParameters:
    inter: HPInter
    intra: Optional[HPIntra] = None
