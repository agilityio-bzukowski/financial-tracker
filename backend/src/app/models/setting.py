from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.db.schema import AIProvider


class SettingsUpdate(BaseModel):
    currency: Optional[str] = None
    ai_provider: Optional[AIProvider] = None
    ai_model: Optional[str] = None


class SettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    currency: str
    ai_provider: AIProvider
    ai_model: str
