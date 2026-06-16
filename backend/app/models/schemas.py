from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    feature: str
    message: str


class ChatResponse(BaseModel):
    message: str
    structured_data: dict | None = None
