import discord 
from discord.ext import commands
from  dotenv import load_dotenv
from os import getenv
import random
import requests
import asyncio
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
SHIVAAY_API_KEY = getenv('SHIVAAY_API_KEY')
DISCORD_BOT_TOKEN = getenv('TOKEN')


SHIVAAY_API_URL = "https://api_v2.futurixai.com/api/lara/v1/completion"
SHIVAAY_API_HEADERS = {
    "Content-Type": "application/json",
    "api-subscription-key": "c2e12f7e-8a45-425e-b303-a230d74f9f25"
}

def get_Lily_Aldrin_response(prompt):
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "Respond like Lily Aldrin to the following and you may use names like Barney ,Robin ,Marshal and Lily sometimes keep it short and concise like not more than 3 lines"
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

punch_lines = ["You son of a beetch!","Where's the poop, Robin?","You can't spell 'Lily' without 'ILY'." 
               "I'm a kindergarten teacher. I can raise you all!",
               "You're dead to me!",
               "I want to say something classy, but that would be a lie!",
               "Oh, honey, you are so cute. And so dumb.",
               "I don't need therapy. I have Marshall!",
               "You broke up with a porn star? Friendship over!",
               "I'm small, but I pack a big punch!",
               "Challenge accepted… Oh wait, that's Barney's thing.",
               "I have a dark side. It's like a little Voldemort.",
               "This is totally going in the scrapbook!",
               "Marshall, we're gonna be rich!",
               "I'm Lily Aldrin and I approve this message."
               ]


bot = commands.Bot(command_prefix ='&',intents =intents)

@bot.event
async def on_ready():
    print(f"logged in as : {bot.user}")

@bot.event 
async def on_message(message):
    print(f"received message: '{message.content}' from: {message.author}")
    await bot.process_commands(message)

@bot.command()
async def hey(ctx):
    respond = random.choice(punch_lines)
    await ctx.reply(respond)

@bot.command()
async def lily(ctx, *, user_message: str):
    try:
        response = await asyncio.to_thread(get_Lily_Aldrin_response, user_message)
        await ctx.reply(response)
    except Exception as e:
        await ctx.reply(f"An error occurred: {e}")

bot.run(getenv('TOKEN'))
