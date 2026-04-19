import torch
from torch.utils.data import Dataset

from app.ai.features.sequence_encoder import SequenceEncoder


class GenomeDataset(Dataset):
    """
    Dataset for:
    sequence → HP_inter prediction
    """

    def __init__(self, sequences, hp_labels):
        self.sequences = sequences
        self.hp_labels = hp_labels

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        seq = self.sequences[idx]
        hp = self.hp_labels[idx]

        x = SequenceEncoder.encode(seq)
        y = torch.tensor(hp, dtype=torch.float32)

        return x, y
