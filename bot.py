import logging
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "ResponseByAi",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        await self.send_message(OWNER_ID, f"**__{me.first_name} is started.....**")
        logger.info(f"Bot {me.first_name} started as @{me.username}")

    async def stop(self, *args):
        await super().stop()
        logger.info("Bot stopped gracefully")

    async def send_admin_log(self, text):
        try:
            await self.send_message(OWNER_ID, text)
        except Exception as e:
            logger.error(f"Failed to send OWNER_ID log: {e}")

if __name__ == "__main__":
    try:
        Bot().run()
    except Exception as e:
        logger.error(f"Bot stopped due to an error: {e}")