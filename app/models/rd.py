import numpy as np
from dataclasses import dataclass


@dataclass
class RD:
    position: np.ndarray
    direction: np.ndarray
