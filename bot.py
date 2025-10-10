# bot_hold.py
import os
import asyncio
import logging
from discord import Intents, Client, Object
from discord.errors import Forbidden, HTTPException, ClientException

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("bot_hold")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
VOICE_CHANNEL_ID = os.getenv("VOICE_CHANNEL_ID")  # ví dụ "123456789012345678"

if not TOKEN or not VOICE_CHANNEL_ID:
    log.error("Env vars DISCORD_BOT_TOKEN và VOICE_CHANNEL_ID phải được thiết lập.")
    raise SystemExit(1)

VOICE_CHANNEL_ID = int(VOICE_CHANNEL_ID)

intents = Intents.default()
# không cần privileged intents cho voice join
client = Client(intents=intents)

# thời gian chờ giữa các lần thử reconnect (giây)
RETRY_DELAY = 10

async def ensure_in_voice():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            # tìm channel từ các guild mà bot hiện có
            channel = None
            for guild in client.guilds:
                ch = guild.get_channel(VOICE_CHANNEL_ID)
                if ch is not None:
                    channel = ch
                    break

            if channel is None:
                log.warning("Không tìm thấy voice channel id=%s trong các guild hiện có. Kiểm tra VOICE_CHANNEL_ID và bot đã được invite chưa.", VOICE_CHANNEL_ID)
                await asyncio.sleep(RETRY_DELAY)
                continue

            # nếu đã kết nối trong guild đó thì giữ, còn không thì connect
            vc = None
            for vc_candidate in client.voice_clients:
                if getattr(vc_candidate.channel, "id", None) == VOICE_CHANNEL_ID:
                    vc = vc_candidate
                    break

            if vc is None:
                try:
                    log.info("Kết nối tới voice channel: %s (%s)", channel.name, VOICE_CHANNEL_ID)
                    vc = await channel.connect(reconnect=True, timeout=30)
                    log.info("Đã kết nối. Giữ im lặng ở channel.")
                except (Forbidden, HTTPException, ClientException) as e:
                    log.exception("Không thể kết nối tới channel: %s", e)
                    await asyncio.sleep(RETRY_DELAY)
                    continue

            # giữ kết nối: chờ trong loop, kiểm tra nếu bị disconnect sẽ lặp lại
            while not client.is_closed() and vc.is_connected():
                await asyncio.sleep(10)

            # Nếu ra khỏi vòng lặp => bị disconnect => hẹn retry
            log.warning("Voice connection bị rời/đóng; sẽ thử reconnect sau %s giây", RETRY_DELAY)
            await asyncio.sleep(RETRY_DELAY)

        except Exception:
            log.exception("Lỗi trong ensure_in_voice loop, sẽ thử lại sau %s giây", RETRY_DELAY)
            await asyncio.sleep(RETRY_DELAY)


@client.event
async def on_ready():
    log.info("Bot ready: %s (id=%s)", client.user, client.user.id)


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(ensure_in_voice())
    try:
        client.run(TOKEN)
    except KeyboardInterrupt:
        log.info("Shutting down.")

if __name__ == "__main__":
    main()
