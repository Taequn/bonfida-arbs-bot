# Bonfida Arbs Bot

A CLI solution to find the arbitrage opportunities between the category-wide bids on [Bonfida](https://sns.id/categories) and Solana Domain Names on [Magic Eden](https://magiceden.io/marketplace/bonfida).


## Getting Started

The things you need before installing the software:
1. Python 3.9+
2. Telegram bot API key (if you want to get notifications to your Telegram)
3. A couple minutes of your time!

## Installing

1. Clone the repository
```
git clone https://github.com/Taequn/bonfida-arbs-bot/tree/CLI_bot
```
2. Run the `docker_launch.sh` script — it will create a Docker image and run the CLI script.
```
./docker_launch.sh
```
3. Alternatively, you can run the script manually:
```
pip install -r requirements.txt
python cli.py
```
4. Follow the instructions upon launch.
5. Enjoy!

## Telegram notifications
1. Create a Telegram bot using [BotFather](https://t.me/botfather)
2. Create settings.json (you can use settings.json.example as a template).
3. Paste your bot API key into the settings.json file.
4. Run the docker_launch.sh script — it will create a Docker image and help you save your chat ID.
```
./docker_launch.sh
```
5. If it's your first launch, you'll need to open your bot and send a /start command.
6. Once that is ready, the script will save your chat ID to the settings.json file.
7. Once the script finds positive arbitrage opportunity, it will send you a message to your Telegram.

## How it works

1. The script uses Bonafida /arbs/ endpoints to pull the information on the category-wide bits and compare those to domains sold on ME.
2. It uses [solana.py](https://michaelhly.github.io/solana-py/) to set up a WebSocket connection to Bonafida program.
3. If there's a new update, the script runs an update function to gather the new information.
4. If there's a positive expected income, the script will open a page where you can buy the domain in one click.
5. The script will also send you a message to your Telegram if you have set up the notifications.

## Future features
1. ✅ Add and web interface and host it online.
2. Add Magic Eden API to pull the information on the domains.
3. Add a function for automatic buying and bidding.

## Contact
If you have any questions or you just want to chat, never hesitate to reach out!

Telegram: @candyflipline

Email: taequn@gmail.com
