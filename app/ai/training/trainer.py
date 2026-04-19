import torch
from torch.utils.data import DataLoader
from tqdm import tqdm


class Trainer:

    def __init__(
        self,
        model,
        train_dataset,
        val_dataset,
        batch_size=32,
        lr=1e-3,
        epochs=10,
        device=None
    ):
        self.device = device or (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )

        self.model = model.to(self.device)

        self.train_loader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
            collate_fn=self.collate_fn
        )

        self.val_loader = DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False,
            collate_fn=self.collate_fn
        )

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = torch.nn.MSELoss()
        self.epochs = epochs

    def collate_fn(self, batch):
        """
        Handles variable-length sequences
        """
        xs, ys = zip(*batch)

        xs_padded = torch.nn.utils.rnn.pad_sequence(
            xs,
            batch_first=True
        )

        ys = torch.stack(ys)

        return xs_padded.to(self.device), ys.to(self.device)

    def train_epoch(self):
        self.model.train()
        total_loss = 0

        for x, y in tqdm(self.train_loader, desc="Training"):
            self.optimizer.zero_grad()

            pred = self.model(x)

            # match shapes if needed
            pred = pred.mean(dim=1)

            loss = self.criterion(pred, y)

            loss.backward()
            self.optimizer.step()

            total_loss += loss.item()

        return total_loss / len(self.train_loader)

    def validate(self):
        self.model.eval()
        total_loss = 0

        with torch.no_grad():
            for x, y in self.val_loader:
                pred = self.model(x)
                pred = pred.mean(dim=1)

                loss = self.criterion(pred, y)
                total_loss += loss.item()

        return total_loss / len(self.val_loader)

    def train(self, save_path="model.pt"):
        best_val_loss = float("inf")

        for epoch in range(self.epochs):
            train_loss = self.train_epoch()
            val_loss = self.validate()

            print(f"Epoch {epoch+1}: Train={train_loss:.4f}, Val={val_loss:.4f}")

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                torch.save(self.model.state_dict(), save_path)
                print("✔ Model saved")
