import uvicorn
from app.config import configs

if __name__ == "__main__":
  uvicorn.run("app.main:app", host="0.0.0.0", port=configs.app_port)