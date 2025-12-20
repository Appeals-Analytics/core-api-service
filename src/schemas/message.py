from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class MessageSchema(BaseModel):
  text: str = Field(..., min_length=1, description="Текст обращения")
  user_id: Optional[str] = Field(None, description="ID пользователя")
  external_id: Optional[str] = Field(None, description="Внешний ID")
  timestamp: Optional[str] = Field(None, description="Время в ISO 8601")
  content_hash: Optional[str] = Field(None, description="SHA-256 hash of timestamp + text")

  @field_validator("text")
  @classmethod
  def text_not_empty(cls, v: str) -> str:
    if not v or not v.strip():
      raise ValueError("text не может быть пустой строкой")
    return v.strip()

  @field_validator("timestamp")
  @classmethod
  def validate_timestamp(cls, v: Optional[str]) -> Optional[str]:
    if v is None or v == "":
      return None
    try:
      datetime.fromisoformat(v.replace("Z", "+00:00"))
      return v
    except (ValueError, AttributeError):
      raise ValueError(f"Неверный формат timestamp: {v}")
