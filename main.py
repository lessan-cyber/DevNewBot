from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from app.config import settings as s
from app.quiz import fetch_quiz, send_quiz, handle_answer
from app.story import get_story_from_gemini, tell_story

async def start(update, context):
    await update.message.reply_text("👋 👋 Je m'appelle Dev News je suis un bot créer par Monsieur AZIZ METCHONOU . je peux vous fournir  \n • des  Quiz sur les langages de programmation\n• une Newsletter quotidienne\n• Des Outils IA hebdomadaires   ")

async def reply(update, context):
    await update.message.reply_text(f" yea bro {update.message.text}")

def main():
    #fetch_quiz()
    application = ApplicationBuilder().token(s.bot_token).build() 
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('quiz', send_quiz))
    application.add_handler(CommandHandler('storyTime', tell_story))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    application.add_handler(CallbackQueryHandler(handle_answer))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()


