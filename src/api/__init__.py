from fastapi import APIRouter
from src.api.files.router import files_router
from src.api.batch_data.router import batch_router
from src.api.dashboard.router import dashboard_router
from src.api.message.router import messages_router
from src.api.filters.router import filters_router

main_router = APIRouter()

main_router.include_router(files_router)
main_router.include_router(batch_router)
main_router.include_router(dashboard_router)
main_router.include_router(messages_router)
main_router.include_router(filters_router)
