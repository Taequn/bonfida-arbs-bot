from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import json
import asyncio

class BonfidaTelegramBot:
    def __init__(self) -> None:
        """
        Initializes the bot, load token, chat_id from settings.json, and add handlers

        Input: None
        Returns: None
        """
        self.__load_token_and_chat_id()
        self.application = ApplicationBuilder().token(self.token).build()
        self.__add_handlers()

    def __load_token_and_chat_id(self) -> None:
        """
        Helper function to load token, chat_id and send updates status from settings.json

        Input: None
        Returns: None
        """
        with open("settings.json", "r") as f:
            info = json.load(f)
        self.token = info["TELEGRAM_BOT_API"]
        self.chat_id = info["TELEGRAM_CHAT_ID"]

    def __add_handlers(self) -> None:
        """
        Helper function to add handlers to the bot

        Input: None
        Returns: None
        """
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))

    def __update_chat_id(self, chat_id: str) -> None:
        """
        Helper function to update chat_id in settings.json if /start is called from a different chat_id

        Input: chat_id
        Returns: None
        """
        self.chat_id = chat_id
        with open("settings.json", "r") as f:
            info = json.load(f)
        info["TELEGRAM_CHAT_ID"] = self.chat_id
        with open("settings.json", "w") as f:
            json.dump(info, f)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Start function, called when /start is called; Saves the chat_id to settings.json

        Input: update, context
        Returns: None
        """

        if self.chat_id != update.effective_chat.id:
            self.__update_chat_id(update.effective_chat.id)

        username = update.effective_chat.username
        message = f"Hello {username}! Your chat ID is {update.effective_chat.id}. We've saved it to settings.json. You can now close this chat and restart the original script!"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Help function, called when /help is called

        Input: update, context
        Returns: None
        """
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Help!")

    async def send_message(self, text: str) -> None:
        """
        Sends a message to the chat_id specified in settings.json

        Input: text
        Returns: None
        """
        await self.application.bot.send_message(chat_id=self.chat_id, text=text)

    def run(self) -> None:
        """
        Runs the bot

        Input: None
        Returns: None
        """
        self.application.run_polling()


if __name__ == "__main__":
    bot = BonfidaTelegramBot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.send_message("Hello"))
