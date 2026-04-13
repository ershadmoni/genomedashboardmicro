from pathlib import Path
from app.models.helical import HPIntra, HPInter, HelicalParameters


class HPReader:

    @staticmethod
    def read(path: Path) -> list[HelicalParameters]:
        if not path.exists():
            raise FileNotFoundError(path)

        hp_list = []

        with path.open() as f:
            lines = f.readlines()

        for line in lines[3:]:
            parts = line.split()

            hp_list.append(
                HelicalParameters(
                    intra=HPIntra(*map(float, parts[1:7])),
                    inter=HPInter(*map(float, parts[7:13]))
                )
            )

        return hp_list
