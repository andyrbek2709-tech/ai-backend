from fastapi import FastAPI
from openai import OpenAI
from supabase import create_client
import os
import uuid

app = FastAPI()

# OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/generate-backend")
async def generate_backend(prompt: dict):
    user_input = prompt.get("text")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты генерируешь backend на FastAPI. Только код."},
            {"role": "user", "content": user_input}
        ]
    )

    code = response.choices[0].message.content

    project_id = str(uuid.uuid4())
    supabase.table("projects").insert({
        "id": project_id,
        "name": user_input,
        "content": code
    }).execute()

    return {
        "id": project_id,
        "code": code
    }


@app.get("/project/{id}")
def get_project(id: str):
    data = supabase.table("projects").select("*").eq("id", id).execute()
    return data.data


@app.get("/projects")
def get_projects():
    data = supabase.table("projects").select("*").execute()
    return data.data
