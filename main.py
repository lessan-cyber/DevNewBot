from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from app.config import settings as s
from app.quiz import  send_quiz, handle_quiz_answer
from app.story import  tell_story
from app.help import help_command, handle_help_answer

async def start(update, context):
    await update.message.reply_text("👋 👋 Je m'appelle Dev News je suis un bot créer par Monsieur AZIZ METCHONOU . je peux vous fournir  \n • des  Quiz sur les langages de programmation\n• une Newsletter quotidienne\n• Des Outils IA hebdomadaires \n taper la commande /help pour en savoir plus  ")

async def reply(update, context):
    await update.message.reply_text(f" yea bro {update.message.text}")
    
application = ApplicationBuilder().token(s.bot_token).build() 
def main():
    #fetch_quiz()
    
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('quiz', send_quiz))
    application.add_handler(CommandHandler('storyTime', tell_story))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    application.add_handler(CallbackQueryHandler(handle_help_answer, pattern="^help_"))
    application.add_handler(CallbackQueryHandler(handle_quiz_answer, pattern="^quiz_"))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()


