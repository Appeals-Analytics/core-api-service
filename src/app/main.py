from fastapi import FastAPI

from api import main_router
from app.utils import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)


