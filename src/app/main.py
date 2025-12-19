from fastapi import FastAPI

from src.api import main_router
from src.app.utils import lifespan

app = FastAPI(lifespan=lifespan, root_path="/api")
app.include_router(main_router)
