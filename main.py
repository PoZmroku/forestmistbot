import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import time

from db import get_voice_minutes, add_voice_minutes

load_dotenv()
TOKEN = os.getenv("TOKEN")


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

voice_sessions = {}

@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} запущен!")

@bot.event
async def on_voice_state_update(member, before, after):
    user_id = str(member.id)

    # Пользователь зашёл в голосовой
    if before.channel is None and after.channel is not None:
        voice_sessions[user_id] = time.time()

    # Пользователь вышел из голосового
    elif before.channel is not None and after.channel is None:
        join_time = voice_sessions.pop(user_id, None)
        if join_time:
            session_duration = int((time.time() - join_time) // 60)  # в минутах
            if session_duration > 0:
                add_voice_minutes(user_id, session_duration)

@bot.command()
async def profile(ctx):
    user_id = str(ctx.author.id)
    minutes = get_voice_minutes(user_id)
    level = minutes // 60
    await ctx.send(f"{ctx.author.mention}, ты провёл {minutes} минут в голосе.\nТвой уровень: {level}")

bot.run(TOKEN)
