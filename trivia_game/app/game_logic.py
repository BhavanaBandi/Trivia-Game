# app/game_logic.py
import requests
import random

# In-memory game state
game_state = {
    "current_question": None,
    "correct_answer": None,
    "score": 0
}

def start_game():
    game_state["score"] = 0
    return {"message": "Game started!", "score": game_state["score"]}

def get_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)
    data = response.json()

    if data["response_code"] == 0:
        question_data = data["results"][0]
        question = question_data["question"]
        correct_answer = question_data["correct_answer"]
        options = question_data["incorrect_answers"] + [correct_answer]
        random.shuffle(options)

        # Save current question and answer
        game_state["current_question"] = question
        game_state["correct_answer"] = correct_answer

        return {
            "question": question,
            "options": options
        }
    else:
        return {"error": "Could not fetch question"}

def submit_answer(user_answer: str):
    correct = game_state.get("correct_answer")

    if not correct:
        return {"error": "No active question. Start the game or fetch a question first."}

    if user_answer.strip().lower() == correct.strip().lower():
        game_state["score"] += 1
        result = "Correct!"
    else:
        result = f"Wrong! The correct answer was: {correct}"

    game_state["correct_answer"] = None  # Reset for next round

    return {
        "result": result,
        "score": game_state["score"]
    }

def get_score():
    return {"score": game_state["score"]}
