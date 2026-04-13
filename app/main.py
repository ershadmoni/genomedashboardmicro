from fastapi import FastAPI
from app.api.routes import geometry, sequence

app = FastAPI(
    title="Genome Dashboard",
    version="1.0.0"
)

app.include_router(
    geometry.router,
    prefix="/geometry",
    tags=["Geometry"]
)

app.include_router(
    sequence.router,
    prefix="/sequence",
    tags=["Sequence"]
)
