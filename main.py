import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

# ====== CONFIG ======
GUILD_ID = 1410339152586870866      # ID server của bạn
CHANNEL_ID = 1410424054481027204    # ID voice channel
TOKEN = os.environ.get("TOKEN")      # Lấy từ Environment Variables trên Render

if not TOKEN:
    print("[ERROR] Please add a bot TOKEN inside Environment Variables.")
    raise SystemExit

# ====== BOT SETUP ======
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print(f"[ERROR] Guild with ID {GUILD_ID} not found.")
        return

    channel = guild.get_channel(CHANNEL_ID)
    if not channel or not isinstance(channel, discord.VoiceChannel):
        print(f"[ERROR] Channel with ID {CHANNEL_ID} not found or not a voice channel.")
        return

    # Nếu bot chưa ở trong kênh thoại → vào
    if not guild.voice_client:
        await channel.connect()
        print(f"🎧 Joined voice channel: {channel.name}")
    else:
        print("ℹ️ Already connected to a voice channel.")

@bot.event
async def on_disconnect():
    print("⚠️ Bot disconnected from Discord!")

# ====== KEEP ALIVE ======
keep_alive()

# ====== RUN BOT ======
try:
    bot.run(TOKEN)
except discord.LoginFailure:
    print("[ERROR] Invalid token. Please double-check your bot token.")
