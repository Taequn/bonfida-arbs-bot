import asyncio
from solana.rpc.websocket_api import connect
from asyncstdlib import enumerate
from solders.pubkey import Pubkey
from solders.errors import SerdeJSONError
from utils.methods import (
    run_arbs_parse,
    display_data_tabulate,
    check_for_positives,
    print_out_dim,
)

class ArbState:
    def __init__(self):
        self.last_positive_name = None

async def run_bot_cli(telegram_bot: bool = False):
    """
    Runs the bot in the command line

    Input: None
    Returns: None
    """
    arb_state = ArbState() # Create an instance of the class to keep track of the last positive name
    while True:
        try:
            df = display_data_tabulate()
            await check_for_positives(df, telegram_status=telegram_bot, arb_state=arb_state) # Check for positives, pass the state
            print_out_dim("Connecting to the websocket")
            program_pub_key = Pubkey.from_string(
                "85iDfUvr3HJyLM2zcq5BXSiDvUWfw6cSE1FfNBo8Ap29"
            )
            async with connect("wss://api.mainnet-beta.solana.com") as websocket:
                print_out_dim("Connected to the websocket")
                await websocket.program_subscribe(program_pub_key)
                print_out_dim("Subscribed to the program")
                first_resp = await websocket.recv()
                async for idx, msg in enumerate(websocket):
                    print_out_dim("Pulled an update!")
                    print_out_dim("Updating...")
                    run_arbs_parse()
                    df = display_data_tabulate()
                    await check_for_positives(df, telegram_status=telegram_bot, arb_state=arb_state)
        except asyncio.exceptions.TimeoutError:
            print_out_dim("Connection timed out. Retrying...")
            continue
        except SerdeJSONError:
            print_out_dim("Connection timed out. Retrying...")
            continue
