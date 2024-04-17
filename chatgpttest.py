import os
from typing import Literal
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key=api_key)

print(f"Key: {api_key}")

system_prompt = "You are a comic book assistant. You reply to the user's question strictly from the perspective of a comic book assistant. If the question is not related to comic books, you politely decline to answer."

class Conversation(BaseModel):
    role: Literal["assistant", "user"]
    content: str

class ConversationHistory(BaseModel):
    history: list[Conversation] = Field ( 
            example = [
                {"role": "user", "content": "tell me a quote from DC comics about life"}
            ]
    )

@app.get("/")
async def health_check():
    return {"status":"ok"}

@app.post("/chat")
async def llm_response(history: ConversationHistory) -> dict:
    # Step 0: Receive the API payload as a dictionary
    history = history.dict()

    # Step 1: Initialize messages with a system prompt and conversation history
    messages = [{"role": "system", "content": system_prompt}, *history["history"]]

    # Step 2: Generate a response
    llm_response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

    # Step 3: Return the generated response and the token usage
    return {
        "message": llm_response.choices[0].message,
        "token_usage": llm_response.usage,
    }
