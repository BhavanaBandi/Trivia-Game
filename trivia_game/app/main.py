# app/main.py
from fastapi import FastAPI, HTTPException
from app.game_logic import start_game, get_question, submit_answer, get_score
import requests
import html,random

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route to serve index.html
@app.get("/play")
def serve_ui():
    return FileResponse(os.path.join("static", "index.html"))


@app.get("/")
def read_root():
    return {"message": "Welcome to the Trivia Game!"}

@app.post("/start")
def start():
    return start_game()

questions = [
    {
        "question": "What company created and developed the game 'Overwatch'?",
        "options": ["Hi-Rez Studios", "Valve", "Blizzard Entertainment", "Gearbox Software"],
        "answer": "Blizzard Entertainment"
    },
    {
        "question": "What is the name of Team Fortress 2's Heavy Weapons Guy's minigun?",
        "options": ["Betty", "Sasha", "Diana", "Anna"],
        "answer": "Sasha"
    },
]

@app.get("/question")
def get_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)
    data = response.json()
    print(data)  # 👈 Add this line to debug

    if data.get("response_code") == 0 and "results" in data and data["results"]:
        question = data["results"][0]
        return {
            "question": question["question"],
            "options": question["incorrect_answers"] + [question["correct_answer"]],
            "answer": question["correct_answer"]
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch trivia question.")
    return {
        "question": question,
        "options": options,
        "answer": correct  # <--- Add this
    }

@app.post("/answer")
def answer(user_answer: str):
    return submit_answer(user_answer)

@app.get("/score")
def score():
    return get_score()
