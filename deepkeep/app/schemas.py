from pydantic import BaseModel

class ChatRequest(BaseModel):
    username: str
    prompt: str

class ChatResponse(BaseModel):
    status: str
    request_id: int
