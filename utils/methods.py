from utils.endpoints import *
import requests
import pandas as pd
import streamlit as st

def empty_dataframe_error():
    return st.warning("No arbitrage opportunities for the given settings.")

# https://sns-api.bonfida.com/v2/arb/me-bonfida?category={category}&max_bid={max_bid}
def get_arbs_me_bonfida(category: str, max_bid: int):
    url = API_URL + f"/v2/arb/me-bonfida?category={category}&max_bid={max_bid}"
    r = requests.get(url)
    return r.json()


def convert_json_to_df(json):
    df = pd.DataFrame(json)
    if df.empty:
        return empty_dataframe_error()
    try:
        df = df.rename(
            columns={
                "domain_name": "Domain Name",
                "expected_profit": "Expected Profit (SOL)",
                "me_price": "Price on Magic Eden (SOL)",
            }
        )
        return st.dataframe(df, width=1000)
    except Exception as e:
        return empty_dataframe_error()

if __name__ == "__main__":
    url = 'https://sns.id/category?category=10k-club'
    r = requests.get(url)