import uvicorn
from fastapi import FastAPI

from config import configs
from api import main_router
from utils import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)


if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=configs.app_port)