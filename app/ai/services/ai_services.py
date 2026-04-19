
from app.ai.inference.predictor import GenomePredictor
from app.models.helical import HPInter


class AIService:

    def __init__(self, model_path: str):
        self.predictor = GenomePredictor(model_path)

    def sequence_to_hp(self, sequence: str):
        """
        Convert DNA sequence → HPInter list
        """
        predictions = self.predictor.predict_hp(sequence)

        hp_list = []

        for p in predictions:
            hp = HPInter(
                shift=p[0],
                slide=p[1],
                rise=p[2],
                tilt=p[3],
                roll=p[4],
                twist=p[5],
            )
            hp_list.append(hp)

        return hp_list
