from app.ai.services.ai_service import AIService
from app.services.geometry_service import GeometryService


class GenomePipeline:

    def __init__(self, model_path: str):
        self.ai_service = AIService(model_path)

    def sequence_to_structure(self, sequence: str):
        """
        Full pipeline:
        Sequence → HP → 3D Structure
        """
        hp_list = self.ai_service.sequence_to_hp(sequence)

        structure = GeometryService.build_structure(hp_list)

        return structure
