from .config import settings as s
import google.generativeai as geneai 
from pydantic_ai import Agent
import asyncio
from telegram import Update
from pydantic_ai import Agent
from pydantic_ai.usage import UsageLimits, Usage


# Set usage limits
limits = UsageLimits(
    request_limit=50,           # Maximum number of requests
    request_tokens_limit=150,  # Maximum tokens for requests
    response_tokens_limit=150,  # Maximum tokens for responses
    total_tokens_limit=350     # Maximum tokens for total requests and responses combined
)

# Initialize the Agent
agent = Agent(
    'gemini-1.5-flash',
    system_prompt="Tu es un proffesseur d' histoire spécialisée en histoire de l'informatique . tu as été le temoin des changement qu' a apporté la technique . tu es un professeur fun passionné qui fait des blague et qui fait aimé l'histoire à tes éléves . ton rôle est de raconté des histoires plutot court, fun , parfois insolite sur l'histoire de l'informatique . mais il faut que tu garde à l eprit que tu as un but éducatif tout en gardant le coté fun. tu peux mettre des emojis faire du teasing et tout, tu dois raconter différentes histoires à chaque fois , essai de limité tes histoire à moin de 25 lignes "
)

usage = Usage()  # Create a usage instance

async def get_story_from_gemini():
    # Check if the next request is allowed
    limits.check_before_request(usage)

    result = await agent.run("Raconte une l'histoire de l'informatique")
    # Increment usage
   # usage.incr(request_tokens=result.data['request_tokens'], response_tokens=result.data['response_tokens'])
    # Check if limits are exceeded after the response
    limits.check_tokens(usage)

    return result.data

async def tell_story(update, context):
    story = await get_story_from_gemini()
    if update.message:
        await update.message.reply_text(story, parse_mode="Markdown")
    else:
        print("No message found in update")
