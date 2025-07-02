from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="OpenAI Secret Service")

class SecretResponse(BaseModel):
    api_key: str

@app.get("/secret", response_model=SecretResponse)
def get_secret():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise HTTPException(status_code=404, detail="API key not found")
    return SecretResponse(api_key=key)
