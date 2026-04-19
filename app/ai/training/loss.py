import torch.nn as nn


class GenomeLoss(nn.Module):
    """
    MSE loss for HP parameters
    """

    def __init__(self):
        super().__init__()
        self.loss = nn.MSELoss()

    def forward(self, pred, target):
        return self.loss(pred, target)
