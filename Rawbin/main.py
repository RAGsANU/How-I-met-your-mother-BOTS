import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import requests
from os import getenv
import google.generativeai as genai
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix ="%",intents =intents)

punch_lines = ["But um, yeah, no.",
               "Nobody asked you, Patrice!",
               "I'm Sparkles, baby!",
               "I'm Canadian. I know how to run from the law.",
               "You guys bang and I'm weird for wanting a pickle?",
               "If I wanted that, I'd just date a Canadian.",
               "I like dogs more than people.",
               "Let's go to the mall… today!",
               "I'm not your bro, bro!",
               "It's Robin 101. The first lesson: I don't like feelings.",
               "I'm a journalist. I say things people don't want to hear.",
               "Suit up? I live up!",
               "You have to let me dance my own battles.",
               "I'm a dirty, dirty girl.",
               "Sorry, but you're just not 'woo' girls."]

genai.configure(api_key=getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash')  

def get_reply(user_message ):
    prompt = f"Respond like Robin Scherbatsky to the following and you may use names like Ted ,barney ,Marshal and Lily sometimes keep it short and concise like not more than 3 lines: {user_message}"
    response = model.generate_content(prompt)
    return response.text


@bot.event
async def on_ready():
    print(f"logged in as : {bot.user}")

@bot.event
async def on_message(message):
    print(f"from {message.author} received message : '{message.content}' ")
    await bot.process_commands(message)


@bot.command()
async def hey(ctx):
    responds = random.choice(punch_lines)
    await ctx.reply(responds)

@bot.command()
async def robin(ctx ,*,user_message :str):
    try:
        
        response = await asyncio.to_thread(get_reply, user_message)
        await ctx.reply(response)
    except Exception as e:
        await ctx.reply(f"An error occurred: {e}")

bot.run(getenv('TOKEN'))