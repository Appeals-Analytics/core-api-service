import uvicorn
from fastapi import FastAPI

from src.config import configs
from src.api import main_router
from src.utils import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)


if __name__ == "__main__":
  uvicorn.run("src.main:app", host="0.0.0.0", port=configs.app_port)