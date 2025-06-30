from keep_alive import keep_alive
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
import time



load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

voice_sessions = {}
DATA_FILE = "voice_data.json"

keep_alive()

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} запущен!")

@bot.event
async def on_voice_state_update(member, before, after):
    data = load_data()
    user_id = str(member.id)

    if before.channel is None and after.channel is not None:
        voice_sessions[user_id] = time.time()
    elif before.channel is not None and after.channel is None:
        join_time = voice_sessions.pop(user_id, None)
        if join_time:
            session_duration = time.time() - join_time
            data[user_id] = data.get(user_id, 0) + session_duration
            save_data(data)


@bot.command()
async def profile(ctx):
    data = load_data()
    user_id = str(ctx.author.id)
    total_seconds = int(data.get(user_id, 0))
    total_minutes = total_seconds // 60
    level = total_minutes // 30
    minutes_for_next = 30 - (total_minutes % 30)

    embed = discord.Embed(
        title=f"🎮 Профиль: {ctx.author.display_name}",
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    embed.add_field(name="⏱ Время в голосе", value=f"{total_minutes} минут", inline=True)
    embed.add_field(name="🏆 Уровень", value=f"{level}", inline=True)
    embed.add_field(name="📈 До след. уровня", value=f"{minutes_for_next} мин", inline=False)

    await ctx.send(embed=embed)


bot.run(TOKEN)
