from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from groq import Groq
import wikipedia

# ---------------- YOUR ORIGINAL CODE STARTS ----------------

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


print("Workout Chatbot (Groq Streaming): Type 'quit', 'exit' or 'bye' to stop\n")

# Tools
def workout_plan_tool(goal: str) -> str:
    goal_lower = goal.lower()
    if "muscle" in goal_lower or "strength" in goal_lower:
        return (
            "Muscle Gain Plan:\n"
            "- Day 1: Chest + Triceps\n"
            "- Day 2: Back + Biceps\n"
            "- Day 3: Shoulders + Abs\n"
            "- Day 4: Legs\n"
            "- Day 5: Rest or Light Cardio\n"
        )
    elif "fat" in goal_lower or "weight loss" in goal_lower:
        return (
            "Fat Loss Plan:\n"
            "- Day 1: HIIT + Full Body\n"
            "- Day 2: Cardio + Core\n"
            "- Day 3: Strength Circuit\n"
            "- Day 4: Cardio + Abs\n"
            "- Day 5: Rest\n"
        )
    else:
        return "Please specify a goal like 'muscle gain' or 'fat loss'."

def exercise_info_tool(exercise: str) -> str:
    try:
        return wikipedia.summary(exercise, sentences=2)
    except Exception:
        return f"No information found for '{exercise}'. Try another exercise."

# ---------------- YOUR ORIGINAL CODE ENDS ----------------

# ---------------- RULE FOR GIRLFRIEND ----------------
    if "girlfriend" in lower_input:
        return JSONResponse({"reply": "My girlfriend is Mahii Shukla ❤️"})
# ---------------- FASTAPI ADDITION ----------------

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat_api(request: Request):
    data = await request.json()
    user_input = data.get("message")

    lower_input = user_input.lower()

    # 1: Workout tool
    if any(k in lower_input for k in ["workout", "plan", "fat", "muscle"]):
        response = workout_plan_tool(user_input)
        return JSONResponse({"reply": response})

    # 2: Exercise info tool
    if any(k in lower_input for k in ["exercise", "how to do", "what is"]):
        response = exercise_info_tool(user_input)
        return JSONResponse({"reply": response})

    # 3: Groq Chat (not streaming here)
    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful workout assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    return JSONResponse({"reply": chat.choices[0].message.content})

