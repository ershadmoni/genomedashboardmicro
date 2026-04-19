import torch
from app.ai.models.genome_transformer import GenomeTransformer
from app.ai.features.sequence_encoder import SequenceEncoder


class GenomePredictor:
    """
    Handles model loading + inference.
    """

    def __init__(self, model_path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = GenomeTransformer()
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    def predict_hp(self, sequence: str):
        """
        Predict helical parameters from sequence.
        """
        with torch.no_grad():
            x = SequenceEncoder.encode(sequence).unsqueeze(0).to(self.device)
            output = self.model(x)

        return output.squeeze(0).cpu().numpy()
