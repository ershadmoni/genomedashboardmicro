import numpy as np

from app.models.rd import RD
from app.utils.geometry import GeometryUtils


class GeometryService:

    @staticmethod
    def hp_to_rd(hp):

        shift = hp.shift
        slide = hp.slide
        rise = hp.rise

        tilt = np.radians(hp.tilt)
        roll = np.radians(hp.roll)
        twist = np.radians(hp.twist)

        displacement = np.array([
            shift,
            slide,
            rise
        ])

        rz = GeometryUtils.rotation_z(twist / 2)
        ry = GeometryUtils.rotation_y(
            np.sqrt(tilt**2 + roll**2)
        )

        transform = rz @ ry

        position = transform @ displacement

        return RD(
            position=position,
            direction=transform
        )

    @staticmethod
    def build_structure(hp_list):

        position = np.zeros(3)
        direction = np.eye(3)

        structure = []

        for hp in hp_list:

            rd = GeometryService.hp_to_rd(hp)

            position = position + direction @ rd.position
            direction = direction @ rd.direction

            structure.append(position.tolist())

        return structure
