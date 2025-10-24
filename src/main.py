import uvicorn
from fastapi import FastAPI

from src.config import configs
from src.api import main_router

app = FastAPI()
app.include_router(main_router)

if __name__ == "__main__":
  uvicorn.run("src.main:app", host="0.0.0.0", port=configs.app_port)