from fastapi import APIRouter
from src.api.files.router import files_router

main_router = APIRouter()

main_router.include_router(files_router)