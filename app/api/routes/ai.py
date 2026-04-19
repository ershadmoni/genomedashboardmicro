from fastapi import APIRouter
from app.ai.pipelines.genome_pipeline import GenomePipeline

router = APIRouter()

pipeline = GenomePipeline(model_path="models/genome_model.pt")


@router.post("/predict-structure")
def predict_structure(sequence: str):
    structure = pipeline.sequence_to_structure(sequence)
    return {"structure": structure}
