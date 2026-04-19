import torch


class SequenceEncoder:
    BASE_MAP = {
        "A": 0,
        "T": 1,
        "C": 2,
        "G": 3,
        "N": 4
    }

    @staticmethod
    def encode(sequence: str) -> torch.Tensor:
        encoded = [
            SequenceEncoder.BASE_MAP.get(base, 4)
            for base in sequence
        ]
        return torch.tensor(encoded, dtype=torch.long)

    @staticmethod
    def batch_encode(sequences):
        return torch.nn.utils.rnn.pad_sequence(
            [SequenceEncoder.encode(seq) for seq in sequences],
            batch_first=True
        )
