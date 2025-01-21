import requests
from app.config import settings as s
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

quiz_cache = []
def fetch_quiz():
    #api_key = s.quiz_api
    url = "https://quizapi.io/api/v1/questions"
    params = {
        "apiKey":s.quiz_api,
        "limit": 5
    }
    try:
        response = requests.get(url, params)
        if response.status_code == 200:
            #print(response.json())
            return(response.json())

        else: 
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"error {e}")
        return []
    
def get_next_quiz():
    global quiz_cache
    # Si le cache est vide ou presque vide, récupérez de nouveaux quiz
    if len(quiz_cache) < 2:
        print("Chargement de nouveaux quiz depuis l'API...")
        new_quizzes = fetch_quiz()
        quiz_cache.extend(new_quizzes)

    # Retournez le prochain quiz du cache
    if quiz_cache:
        return quiz_cache.pop(0)  # Retire et retourne le premier quiz
    else:
        print("Aucun quiz disponible")
        return None

def get_correct_answer_key(correct_answers):
    for key, value in correct_answers.items():
        if value == 'true':
            print(key)
            return key
    return None

async def send_quiz(update, context):
    quiz = get_next_quiz()
    print(quiz)
    if quiz:
        question = quiz["question"]
        answers = quiz["answers"]
        correct_answers = quiz["correct_answers"]
        correct_answer_key = get_correct_answer_key(correct_answers)[:8]
        print(correct_answer_key)

        if correct_answer_key:
            #correct_answer = answers.get(correct_answer_key)
            #print(correct_answer)
            for key, value in answers.items():
                if key == correct_answer_key:
                    correct_answer = value
        else:
            correct_answer = None

        message = f"**Question**: {question}\n\n"
        keyboard = []
        for key, value in answers.items():
            if value:  # Vérifiez que la réponse n'est pas None
                keyboard.append([InlineKeyboardButton(value, callback_data=key)])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")
        print(correct_answer)
        # Store the correct answer in user data
        context.user_data["correct_answer"] = correct_answer
        context.user_data["correct_answer_key"] = correct_answer_key
    else:
        await update.message.reply_text("Aucun quiz disponible pour le moment.")

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_answer = query.data
    correct_answer = context.user_data.get("correct_answer")
    correct_answer_key = context.user_data.get("correct_answer_key")
    if correct_answer is None:
        await query.edit_message_text("Erreur: La réponse correcte n'a pas été trouvée.")
        return

    if user_answer == correct_answer_key:
        await query.edit_message_text("Bonne réponse ! 🎉")
    else:
        await query.edit_message_text(f"Mauvaise réponse 😢 La bonne réponse était : {correct_answer}")

    # Supprimer la bonne réponse après traitement
    context.user_data.pop("correct_answer", None)
    context.user_data.pop("correct_answer_key", None)

