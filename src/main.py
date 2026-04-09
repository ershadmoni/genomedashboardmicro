from fastapi import FastAPI
from fastapi.background import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from server.genomeserver import genome_router_v1

app = FastAPI()
app.include_router(genome_router_v1, prefix="/v1")

