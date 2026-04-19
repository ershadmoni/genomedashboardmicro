from sklearn.model_selection import train_test_split

from app.ai.models.genome_transformer import GenomeTransformer
from app.ai.datasets.genome_dataset import GenomeDataset
from app.ai.training.trainer import Trainer


class TrainingPipeline:

    def __init__(self, sequences, hp_labels):
        self.sequences = sequences
        self.hp_labels = hp_labels

    def run(self):

        X_train, X_val, y_train, y_val = train_test_split(
            self.sequences,
            self.hp_labels,
            test_size=0.2,
            random_state=42
        )

        train_dataset = GenomeDataset(X_train, y_train)
        val_dataset = GenomeDataset(X_val, y_val)

        model = GenomeTransformer()

        trainer = Trainer(
            model=model,
            train_dataset=train_dataset,
            val_dataset=val_dataset,
            epochs=20
        )

        trainer.train(save_path="models/genome_model.pt")
