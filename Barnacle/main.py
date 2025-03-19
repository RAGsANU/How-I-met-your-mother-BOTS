import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
import random
import google.generativeai as genai  
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

punch_lines = [
    "Suit up!",
    "Challenge accepted!",
    "It's gonna be legendary... wait for it... dary! Legendary!",
    "Haaaave you met Ted?",
    "When I get sad, I stop being sad and be awesome instead. True story.",
    "New is always better.",
    "Think of me like Yoda, but instead of being little and green, I wear suits and I'm awesome. I'm your bro — I'm Broda!",
    "I'm not a father. That would take all the fun out of being Uncle Barney.",
    "Step one: lose the bra. Step two: cheer up. Step three: lose the bra.",
    "God, it's me, Barney. What up?",
    "You can't spell legendary without 'dary'.",
    "A bro is always entitled to do something stupid, as long as the rest of his bros are all doing it.",
    "I'm awesome. You know why? Because I just am.",
    "Suit up. It's not just a saying, it's a lifestyle."
]


genai.configure(api_key=getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash')  

def get_reply(user_message ):
    prompt = f"Respond like Barney Stinson to the following and you may use names like Ted ,Robin ,Marshal and Lily sometimes keep it short and concise like not more than 3 lines: {user_message}"
    response = model.generate_content(prompt)
    return response.text



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    print(f"Received message :'{message.content}' from {message.author}")
    await bot.process_commands(message)

@bot.command()
async def hey(ctx):
    respond = random.choice(punch_lines)
    await ctx.reply(respond)


@bot.command()
async def barney(ctx, *, user_message: str ):
    try:
        
        response = await asyncio.to_thread(get_reply, user_message)
        await ctx.reply(response)
    except Exception as e:
        await ctx.reply(f"An error occurred: {e}")


bot.run(getenv('TOKEN'))