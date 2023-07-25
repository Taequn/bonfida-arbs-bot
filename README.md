# Bonfida Arbs Bot

A CLI solution to find the arbitrage opportunities between the category-wide bids on [Bonfida](https://sns.id/categories) and Solana Domain Names on [Magic Eden](https://magiceden.io/marketplace/bonfida).


## Getting Started

The things you need before installing the software:
1. Python 3.9+
2. A couple minutes of your time!

### Installing

1. Clone the repository
```
git clone https://github.com/Taequn/bonfida-arbs-bot/tree/CLI_bot
```
2. Open the folder
```
cd bonfida-arbs-bot
```
3. Create virtual environment
```
pip install virtualenv
python3.9 -m venv env
source env/bin/activate
```
4. Install the packages
```
pip install -r requirements
```
5. Run the script
```
python run.py
```

## How it works

1. The script uses Bonafida /arbs/ endpoints to pull the information on the category-wide bits and compare those to domains sold on ME.
2. It uses [solana.py](https://michaelhly.github.io/solana-py/) to set up a WebSocket connection to Bonafida program.
3. If there's a new update, the script runs an update function to gather the new information.
4. If there's a positive expected income, the script will open a page where you can buy the domain in one click.

## Contact
If you have any questions or you just want to chat, never hesitate to reach out!
Telegram: @candyflipline
Email: taequn@gmail.com
