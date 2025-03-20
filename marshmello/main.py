import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
from os import getenv
import requests
import google.generativeai as genai
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "!",intents=intents)

punch_lines = ["Lawyered!",
               "You just got slapped!",
               "I can jump really high.",
               "You can't just skip the sad part. You have to let yourself grieve.",
               "This is totally going in the Slap Bet countdown!",
               "I'm not scared of Sasquatch. I am Sasquatch!",
               "I have a thing for charts.",
               "Oh, look at me, the millionaire who goes to see doctors!",
               "That is the dream. To make it as a Big Fudge.",
               "It's not a lie if you believe it.",
               "Pause.",
               "I'm gonna go eat ribs with my dad. It's gonna be legen... wait for it... dary!",
               "I'm Marshall, and I love food!","Minnesota will always be my home.","I am the kid who had the 102-pound pumpkin in fourth grade. I am Big Fudge!"]

genai.configure(api_key=getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash')  

def get_reply(user_message ):
    prompt = f"Respond like Marshal Eriksen to the following and you may use names like Ted ,barney ,Robin and Lily sometimes keep it short and concise like not more than 3 lines: {user_message}"
    response = model.generate_content(prompt)
    return response.text

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

@bot.event 
async def on_message(message):
    print(f"message received : '{message.content}' from : {message.author}")
    await bot.process_commands(message)

@bot.command()
async def hey(ctx):
    respond = random.choice(punch_lines)
    await ctx.reply(respond)

@bot.command()
async def marshal(ctx ,*,user_message:str):
    try:
        response = await asyncio.to_thread(get_reply, user_message)
        await ctx.reply(response)
    except Exception as e:
        await ctx.reply(f"An error occurred: {e}")

bot.run(getenv('TOKEN'))