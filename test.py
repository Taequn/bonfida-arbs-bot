import asyncio
from solana.rpc.async_api import AsyncClient
from solana.rpc.websocket_api import connect
from asyncstdlib import enumerate

from solana.rpc.types import MemcmpOpts
from solders.pubkey import Pubkey
from solders.signature import Signature
import json


async def main_async():
    program_pub_key = Pubkey.from_string("85iDfUvr3HJyLM2zcq5BXSiDvUWfw6cSE1FfNBo8Ap29")

    async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
        res = await client.is_connected()
        program_signatures = await client.get_signatures_for_address(
            program_pub_key, limit=5
        )
        program_signatures = json.loads(program_signatures.to_json())
        results = program_signatures["result"]
        filter_opts = MemcmpOpts(offset=0, bytes="C")

        trans_sign = Signature.from_string(results[0]["signature"])
        trans = await client.get_transaction(trans_sign)
        trans = json.loads(trans.to_json())
        trans_results = trans["result"]
        for x in trans_results:
            print(x)
            print(trans_results[x])
            print()


# asyncio.run(main_async())


async def main():
    # program_pub_key = Pubkey.from_string("5Y1VqvwH5ep9JGJ4hhzxFoupy5Ndkk49ggKpWqAcjszs")
    program_pub_key = Pubkey.from_string("85iDfUvr3HJyLM2zcq5BXSiDvUWfw6cSE1FfNBo8Ap29")
    async with connect("wss://api.mainnet-beta.solana.com") as websocket:
        await websocket.account_subscribe(program_pub_key)
        first_resp = await websocket.recv()
        subscription_id = first_resp[0].result
        async for idx, msg in enumerate(websocket):
            print(idx)
            print(msg)


asyncio.run(main())
