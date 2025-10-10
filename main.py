import discord
import asyncio
import os

TOKEN = os.getenv("TOKEN")  # Lấy token từ Render environment variable
VOICE_CHANNEL_ID = int(os.getenv("1408816880730247329"))  # ID kênh voice

intents = discord.Intents.default()
client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    # Kết nối voice channel
    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            await channel.connect()
            print(f"🔊 Joined voice channel: {channel.name}")
        except discord.ClientException:
            print("⚠️ Already connected to a voice channel.")
    else:
        print("❌ Voice channel not found! Check the ID or bot permissions.")
# Giữ bot chạy (loop vô hạn)
async def keep_alive_loop():
    while True:
        await asyncio.sleep(60)
@client.event
async def on_disconnect():
    print("⚠️ Bot disconnected! Render sẽ tự restart.")
async def main():
    async with client:
        await asyncio.gather(client.start(TOKEN), keep_alive_loop())
if __name__ == "__main__":
    asyncio.run(main())
