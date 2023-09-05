import asyncio
from utils.methods import init_message
from utils.websocket import run_bot_cli
from notifications.bot_init import init_tg_bot

'''
This is the main file of the project.

Here we initialize the message that will be displayed when the bot is started.
We also initialize if the bot will be started with the telegram bot or not.

Finally, we connect to the websocket and start the bot.
'''

init_message()
tg_bot_status = init_tg_bot()

asyncio.run(run_bot_cli(telegram_bot=tg_bot_status))
