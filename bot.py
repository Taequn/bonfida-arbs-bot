import asyncio
from solana.rpc.websocket_api import connect
from asyncstdlib import enumerate
from solders.pubkey import Pubkey
from utils.methods import (
    run_arbs_parse,
    display_data_tabulate,
    check_for_positives,
    print_out_dim,
    init_message,
)

init_message()


async def run_bot():
    while True:
        try:
            df = display_data_tabulate()
            check_for_positives(df)
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
                    check_for_positives(df)
        except asyncio.exceptions.TimeoutError:
            print_out_dim("Connection timed out. Retrying...")
            continue
        except Exception as e:
            print_out_dim("Connection error. Reconnecting...")
            continue


asyncio.run(run_bot())
