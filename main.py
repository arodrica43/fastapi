from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"endpoints": {
        "/user": "CRUD user"
    }}

class User(BaseModel):
    name: str
    email: str
    password: str

@app.post("/user")
def create_user(user: User):
    # TO DO: Real persistence
    return user

@app.get("/user/{user_email}")
def read_item(user_email: str, q: Optional[str] = None):
    # TO DO: Real search
    return {"user_email": user_email, "q": q}