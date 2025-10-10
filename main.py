import discord
import asyncio
import os
from keep_alive import keep_alive

TOKEN = os.getenv("TOKEN")
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID", "0"))  # đặt ID voice channel trong Render

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            await channel.connect()
            print(f"🎧 Joined voice channel: {channel.name}")
        except Exception as e:
            print(f"⚠️ Could not join channel: {e}")
    else:
        print("⚠️ Voice channel not found or invalid ID!")

keep_alive()
client.run(TOKEN)
