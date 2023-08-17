import asyncio
from utils.methods import init_message
from utils.websocket import run_bot_cli

init_message()
asyncio.run(run_bot_cli())
