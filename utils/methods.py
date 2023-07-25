from utils.endpoints import *
import requests
import pandas as pd
import streamlit as st
from utils.constants import CATEGORIES_DICTIONARY_INVERTED, CATEGORIES_DICTIONARY
from datetime import datetime, timedelta
import logging
from tabulate import tabulate
import webbrowser
from colorama import Style, init, Fore

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

    for index, row in df.iterrows():
        print_out_dim(f"Processing {index} of {df_length}")
        category = row["category"]
        try:
            print_out_dim(f"Processing: {category}")
            min_price = get_min_price_me_category(category)
            me_price = min_price["me_price"]
            domain_name = min_price["domain_name"]
            df.at[index, "domain_name"] = domain_name
            df.at[index, "me_price"] = me_price
        except:
            print_out_dim(f"{category}: no results for the category.")
            df.drop(index, inplace=True)
            continue
    df["expected_profit"] = round(df["sol_price"] - df["me_price"], 2)
    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv("data/best_bids_with_me.csv")


def dataframe_prettify(df: pd.DataFrame):
    # select columns: category, sol_price, domain_name, me_price, expected_profit
    df = df[["category", "sol_price", "domain_name", "me_price", "expected_profit"]]
    # rename columns
    df = df.rename(
        columns={
            "category": "Category",
            "sol_price": "Bonfida Price",
            "domain_name": "Domain Name",
            "me_price": "Magic Eden Price",
            "expected_profit": "Expected Profit",
        }
    )
    df = df.sort_values(by="Expected Profit", ascending=False)

    return df


def run_arbs_parse():
    get_all_arbs()
    get_all_arbs_opportunities()


def display_data_tabulate():
    try:
        df = pd.read_csv("data/best_bids_with_me.csv")
    except FileNotFoundError:
        print_out_dim("No data found. Updating...")
        run_arbs_parse()
        df = pd.read_csv("data/best_bids_with_me.csv")
    
    last_updated = df["timestamp"].iloc[0]
    last_updated = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
    #if last_updated more than 20 minutes ago, run_arbs_parse()
    if last_updated < datetime.now() - timedelta(minutes=20):
        print_out_dim("Data is more than 20 minutes old. Updating...")
        print_out_dim("This will take ~2 minutes.")
        run_arbs_parse()
        df = pd.read_csv("data/best_bids_with_me.csv")
        last_updated = df["timestamp"].iloc[0]
    
    
    df_pretty = dataframe_prettify(df)
    print_out_dim(tabulate(df_pretty, headers="keys", tablefmt="psql", showindex=False))  # type: ignore
    
    print_out_dim(f"Last updated: {last_updated}")
    return df


def check_for_positives(df: pd.DataFrame):
    if df["expected_profit"].max() > 0:
        print_out_dim("Positive arbs found")
        name = df["Domain Name"].iloc[0]
        url = "https://sns.id/search?search=" + name.strip()
        webbrowser.open(url)
    else:
        print_out_dim("No positive arbs found")


def get_time():
    now = datetime.now()
    date_format = now.strftime("[%d/%m/%Y  %H:%M:%S]")
    return date_format


def print_out_dim(text: str):
    print(f"{Style.DIM}{get_time()} {text}.{Style.RESET_ALL}")


def init_message():
    print(
        f" \n{Fore.BLUE}{Style.BRIGHT}BONFIDA ARBS CLI BOT{Style.RESET_ALL}\n \nGithub: Taequn\nTwitter: @candyflipline\nTelegram: @candyflipline\n"
    )


if __name__ == "__main__":
    run_arbs_parse()
