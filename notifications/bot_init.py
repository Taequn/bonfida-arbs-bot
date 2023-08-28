import json
import os
from utils.methods import print_out_dim
from notifications.telegram_bot import BonfidaTelegramBot


def init_tg_bot() -> bool:
    """
    Initializes the telegram bot by reading the config file and creating a telegram bot object

    Input: None
    Returns: None
    """
    # Check if config file exists
    if not os.path.exists("settings.json"):
        print_out_dim(
            "No settings.json file found. Do you want to use Telegram bot? (y/n)"
        )
        while True:
            answer = input()
            if answer == "y":
                create_settings_file()
                break
            elif answer == "n":
                print_out_dim("Telegram bot will not be used.")
                return False
            else:
                print_out_dim("Invalid input. Please enter y or n.")

    with open("settings.json", "r") as f:
        info = json.load(f)

    if info["TELEGRAM_BOT_API"] == "":
        # Throw an exception if the API key is not found
        raise ValueError(
            "No Telegram bot API key found. You'll need to create a Telegram bot with BotFather and enter the API key in the settings.json file."
        )

    if info["TELEGRAM_CHAT_ID"] == "":
        print_out_dim(
            "No Telegram chat ID found. You'll need to save it with the /start command in the Telegram bot."
        )
        print_out_dim("===========================================\n")
        print_out_dim("INSTRUCTIONS:")
        print_out_dim("1. Go to the Telegram bot you created with BotFather.")
        print_out_dim("2. Send the /start command to the bot.")
        print_out_dim(
            "3. Restart the script after — your chat ID will be automatically saved!\n"
        )
        print_out_dim("===========================================")

        bot = BonfidaTelegramBot()
        bot.run()

    print_out_dim("Telegram bot initialized")
    print_out_dim(f'Chat ID: {info["TELEGRAM_CHAT_ID"]}')
    return True


def create_settings_file() -> None:
    """
    Creates a settings.json file with the default settings

    Input: None
    Returns: None
    """
    # {"TELEGRAM_BOT_API": "YOUR_API_KEY", "TELEGRAM_CHAT_ID": ""}
    settings = {"TELEGRAM_BOT_API": "", "TELEGRAM_CHAT_ID": ""}
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)
    print_out_dim(
        "settings.json file created. Please fill in the token and chat_id fields."
    )
