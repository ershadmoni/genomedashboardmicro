import torch
import torch.nn as nn


class GenomeTransformer(nn.Module):
    """
    Transformer model to predict HP_inter from DNA sequence.
    """

    def __init__(
        self,
        vocab_size: int = 5,   # A, T, C, G, N
        d_model: int = 128,
        nhead: int = 8,
        num_layers: int = 4
    ):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, d_model)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )

        self.fc = nn.Linear(d_model, 6)  # HP_inter (6 params)

    def forward(self, x):
        """
        x: (batch, seq_len)
        """
        x = self.embedding(x)
        x = self.transformer(x)
        return self.fc(x)
