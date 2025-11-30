from pydantic import BaseModel
from datetime import datetime


class AppealItem(BaseModel):
    user_id: str
    external_id: str
    text: str
    timestamp: datetime
