import discord
import os
from keep_alive import keep_alive

# Lấy biến môi trường từ Render Dashboard
TOKEN = os.getenv("TOKEN")
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID", "0"))  # fallback = 0 nếu chưa set

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    if not VOICE_CHANNEL_ID:
        print("⚠️ VOICE_CHANNEL_ID not set! Please add it to Environment Variables.")
        return

    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            await channel.connect()
            print(f"🎧 Joined voice channel: {channel.name}")
        except Exception as e:
            print(f"⚠️ Failed to join voice channel: {e}")
    else:
        print("❌ Voice channel not found or invalid ID.")

keep_alive()
client.run(TOKEN)
