import discord
import asyncio
from keep_alive import keep_alive
import os

TOKEN = os.getenv("TOKEN")
VOICE_CHANNEL_ID = 1408816880730247329  # thay ID voice channel của bạn

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        await channel.connect()
        print(f"✅ Joined voice channel: {channel.name}")
    else:
        print("⚠️ Voice channel not found!")

keep_alive()  # khởi động web server keep-alive
client.run(TOKEN)

