import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
import random
import asyncio
import requests

load_dotenv()


SHIVAAY_API_KEY = getenv('SHIVAAY_API_KEY')
DISCORD_BOT_TOKEN = getenv('TOKEN')


SHIVAAY_API_URL = "https://api_v2.futurixai.com/api/lara/v1/completion"
SHIVAAY_API_HEADERS = {
    "Content-Type": "application/json",
    "api-subscription-key": "c2e12f7e-8a45-425e-b303-a230d74f9f25"
}

def get_ted_mosby_response(prompt):
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "Respond like Ted Mosby to the following and you may use names like Barney ,Robin ,Marshal and Lily sometimes keep it short and concise like not more than 3 lines"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "top_p": 1
    }
    response = requests.post(SHIVAAY_API_URL, headers=SHIVAAY_API_HEADERS, json=payload, verify=False)
    if response.status_code == 200:
        return response.json()['answer']
    else:
        return f"Error: {response.status_code}"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='^', intents=intents)

punch_lines = [
    "I'm not a hero. I'm a guy who was just in the right place at the right time... with a sword.",
    "Nothing good happens after 2 AM.",
    "You can't design your life like a building. It doesn't work that way. You just have to live it and it'll design itself.",
    "I think I was too in love with her to break up with her.",
    "If you're not scared, you're not taking a chance. And if you're not taking a chance, what the hell are you doing anyway?",
    "Everyone has an opinion on how long it takes to recover from a breakup.",
    "The great moments of your life won't necessarily be the things you do. They'll also be the things that happen to you.",
    "Shouldn't we hold out for the person who doesn't just tolerate our little quirks but actually kinda likes them?",
    "Sometimes things have to fall apart to make way for better things.",
    "I used to believe in destiny, you know? I'd go to the bagel place, see a pretty girl in line, and think, Maybe she's the one.",
    "Because sometimes, even if you know how something's gonna end, that doesn't mean you can't enjoy the ride.",
    "Look, our story is just beginning.",
    "Love is the best thing we do.",
    "When you love someone, you just… you don't stop. Ever.",
    "Kids, you can't cling to the past. Because no matter how tightly you hold on, it's already gone."
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    print(f"received message: '{message.content}' from {message.author}")
    await bot.process_commands(message)

@bot.command()
async def hey(ctx):
    respond = random.choice(punch_lines)
    await ctx.reply(respond)

@bot.command()
async def ted(ctx, *, user_message: str):
    try:
        response = await asyncio.to_thread(get_ted_mosby_response, user_message)
        await ctx.reply(response)
    except Exception as e:
        await ctx.reply(f"An error occurred: {e}")

bot.run(DISCORD_BOT_TOKEN)