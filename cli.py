import asyncio
from utils.methods import init_message
from utils.websocket import run_bot_cli
from notifications.bot_init import init_tg_bot

init_message()
tg_bot_status = init_tg_bot()

asyncio.run(run_bot_cli(telegram_bot=tg_bot_status))
