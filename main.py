from fastapi import FastAPI
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/generate-backend")
async def generate_backend(prompt: dict):
    user_input = prompt.get("text")

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты генерируешь backend на FastAPI. Только код."},
            {"role": "user", "content": user_input}
        ]
    )

    return {"code": response.choices[0].message.content}