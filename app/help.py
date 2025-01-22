from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from .quiz import send_quiz
from .story import tell_story, get_story_from_gemini
async def help_command(update, context):
    message = "Taper la commande :\n"
    list_of_commands = {
        "/quiz": "Taper la commande /quiz pour pour faire un quiz sur l'informatique",
        "/storyTime": "Taper /storyTime Pour avoir un fun fact sur l'histoire de l'informatique"
    }
    try: 
        keyboard = []
        for key, value in list_of_commands.items():
            keyboard.append([InlineKeyboardButton(value,callback_data=f"help_{key}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")
    except Exception as e:
        print(f"Error {e}")

async def handle_help_answer(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    #print(query)
    command = query.data.replace("help_", "")
    print(f"Callback received: {command}")
    await query.answer() 
 
    if command == "/quiz":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Starting quiz...")
        await send_quiz(query, context)

    elif command == "/storyTime":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Here's a fun fact about the history of computing...")
        #await get_story_from_gemini()
        await tell_story(query, context)
 
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown command.")
