from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from groq import Groq
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("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"))  # API key from .env

# Templates folder
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    response_text = ""

    # Stream Groq responses
    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful workout chatbot."},
            {"role": "user", "content": user_input}
        ],
        stream=True
    )

    # Collect response
    for chunk in stream:
        delta = chunk.choices[0].delta
        if hasattr(delta, "content") and delta.content:
            response_text += delta.content
            await asyncio.sleep(0)  # async-friendly

    return {"response": response_text}
