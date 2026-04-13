from fastapi import APIRouter

genome_router_v1 = APIRouter(prefix = "/resources", tags=["resources"])

@genome_router_v1.get("/resource/{HP_intra}, {HP_inter}", description="Getting HP data...")
async def get_HP(HP_intra : str, HP_inter : str):
    return f"We have : {HP_intra, HP_inter}"