import uvicorn
from src.app.config import configs

if __name__ == "__main__":
  uvicorn.run("src.app.main:app", host="0.0.0.0", port=configs.app_port, reload=True)
