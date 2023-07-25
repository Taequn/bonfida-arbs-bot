from utils.endpoints import *
import requests
import pandas as pd
import streamlit as st
from utils.constants import CATEGORIES_DICTIONARY_INVERTED, CATEGORIES_DICTIONARY
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_all_arbs():
    url = API_URL + "/v2/arb/category-best-bid"
    r = requests.get(url)
    json_object = r.json()
    df = pd.DataFrame(json_object).T
    df.index.name = "category"
    df.to_csv("data/best_bids.csv")


def get_arbs_me_bonfida(category: str, max_bid: int):
    url = API_URL + f"/v2/arb/me-bonfida?category={category}&max_bid={max_bid}"
    r = requests.get(url)
    json_object = r.json()
    df = pd.DataFrame(json_object)
    return df


def get_min_price_me_category(category: str):
    df = get_arbs_me_bonfida(category, 90000)
    df["category"] = category
    min_price = df["me_price"].idxmin()
    return_df = df.loc[min_price]
    return return_df


def get_all_arbs_opportunities():
    df = pd.read_csv("data/best_bids.csv")
    df_length = len(df)
    df["domain_name"] = ""
    df["me_price"] = 0

    my_bar = st.sidebar.progress(0)
    current_listing = st.sidebar.empty()

    for index, row in df.iterrows():
        logger.info(f"Processing {index} of {df_length}")
        category = row["category"]
        try:
            current_listing.text(f"Processing: {category}")
            my_bar.progress((index + 1) / df_length) #type: ignore
            min_price = get_min_price_me_category(category)
            me_price = min_price["me_price"]
            domain_name = min_price["domain_name"]
            df.at[index, "domain_name"] = domain_name
            df.at[index, "me_price"] = me_price
        except:
            logger.info(f"Error with {category}: df is empty")
            df.drop(index, inplace=True)
            continue
    df["expected_profit"] = round(df["sol_price"] - df["me_price"], 2)
    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv("data/best_bids_with_me.csv")
    
def dataframe_prettify(df: pd.DataFrame):
    #select columns: category, sol_price, domain_name, me_price, expected_profit
    df = df[["category", "sol_price", "domain_name", "me_price", "expected_profit"]]
    #rename columns
    df = df.rename(columns={
        "category": "Category",
        "sol_price": "Bonfida Price",
        "domain_name": "Domain Name",
        "me_price": "Magic Eden Price",
        "expected_profit": "Expected Profit"
    })
    df = df.sort_values(by="Expected Profit", ascending=False)
    
    return df
    
    


def run_arbs_parse():
    get_all_arbs()
    get_all_arbs_opportunities()


if __name__ == "__main__":
    run_arbs_parse()
