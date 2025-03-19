import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix ="%",intents =intents)

@bot.event
async def on_ready()
    print(f"loggedf in as : {bot.user}")


@bot.command()
async def hey(ctx)
    await ctx.reply()
