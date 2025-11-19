from fastapi import APIRouter
from src.api.files.router import files_router
from src.api.batch_data.router import batch_router

main_router = APIRouter()

main_router.include_router(files_router)
main_router.include_router(batch_router)
