import requests
from app.config import settings as s
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

quiz_cache = []

def fetch_quiz():
    url = "https://quizapi.io/api/v1/questions"
    params = {
        "apiKey": s.quiz_api,
        "limit": 5
    }
    try:
        response = requests.get(url, params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"error {e}")
        return []

def get_next_quiz():
    global quiz_cache
    if len(quiz_cache) < 2:
        print("Chargement de nouveaux quiz depuis l'API...")
        new_quizzes = fetch_quiz()
        quiz_cache.extend(new_quizzes)

    if quiz_cache:
        return quiz_cache.pop(0)
    else:
        print("Aucun quiz disponible")
        return None

def get_correct_answer_key(correct_answers):
    for key, value in correct_answers.items():
        if value == 'true':
            return key
    return None

async def send_quiz(update, context):
    quiz = get_next_quiz()
    if quiz:
        question = quiz["question"]
        answers = quiz["answers"]
        correct_answers = quiz["correct_answers"]
        correct_answer_key = get_correct_answer_key(correct_answers)[:8]
        for key , value in answers.items():
            if key == correct_answer_key:
                correct_answer = value

        print(correct_answer)
        message = f"**Question**: {question}\n\n"
        keyboard = []
        for key, value in answers.items():
            if value:
                keyboard.append([InlineKeyboardButton(value, callback_data=f"quiz_{key}")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")
        context.user_data["correct_answer"] = correct_answer
        context.user_data["correct_answer_key"] = correct_answer_key
    else:
        await update.message.reply_text("Aucun quiz disponible pour le moment.")

async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_answer = query.data
    correct_answer = context.user_data.get("correct_answer")
    correct_answer_key = context.user_data.get("correct_answer_key")

    if correct_answer is None:
        await query.edit_message_text("Erreur: La réponse correcte n'a pas été trouvée.")
        return

    if user_answer == f"quiz_{correct_answer_key}":
        await query.edit_message_text("Bonne réponse ! 🎉")
    else:
        await query.edit_message_text(f"Mauvaise réponse 😢 La bonne réponse était : {correct_answer}")

    context.user_data.pop("correct_answer", None)
    context.user_data.pop("correct_answer_key", None)

