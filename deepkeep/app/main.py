import re

import httpx
from fastapi import FastAPI, HTTPException

from app import models, crud
from app.constants import OPENAI_API_KEY
from app.database import engine, get_db_session
from app.schemas import ChatRequest, ChatResponse

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    with get_db_session() as db:
        user = crud.get_user(db, req.username)
        if not user:
            user = crud.create_user(db, req.username)
        crud.unblock_expired(db, user)

        if user.blocked:
            raise HTTPException(status_code=403, detail="User is blocked")

        mentions = re.findall(r"@(\w+)", req.prompt)
        mentions = [m for m in mentions if m != req.username]
        if mentions:
            crud.increment_mentions(db, user, len(mentions))
            if user.blocked:
                raise HTTPException(status_code=403, detail="User is now blocked")

        chat_req = crud.create_request(db, user.id, req.prompt)

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        payload = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": req.prompt}]}
        response = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        result = response.json()["choices"][0]["message"]["content"]

    with get_db_session() as db:
        crud.save_result(db, chat_req.id, result)

    return ChatResponse(status=result, request_id=chat_req.id)


from fastapi import Path

@app.post("/unblock/{username}")
def unblock_user(username: str = Path(...)):
    with get_db_session() as db:
        user = crud.get_user(db, username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        crud.unblock_user(db, user)
        return {"message": f"User {username} has been unblocked"}
