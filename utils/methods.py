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
from rich.console import Console
from rich.table import Table
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

console = Console()

def get_all_arbs() -> pd.DataFrame:
    """
    Makes a request to the API and returns a dataframe of all the best bids for each category

    Input: None
    Returns: dataframe of all the best bids for each category
    """
    url = API_URL + "/v2/arb/category-best-bid"
    r = requests.get(url)
    json_object = r.json()
    df = pd.DataFrame(json_object).T
    df.reset_index(inplace=True)
    df.columns = ["category", "nb_domains", "sol_price"]
    return df


def get_arbs_list(df: pd.DataFrame) -> list:
    """
    Helper function to get the list of categories from the dataframe

    Input: dataframe of all the best bids for each category
    Returns: list of categories
    """
    return df["category"].tolist()


def get_all_me_listings(list_of_categories: list) -> pd.DataFrame:
    """
    Makes a request to the API and returns a dataframe of all the Magic Eden listings for each category
    Iterates through the list of categories in chunks of 25 to avoid hitting the API return limit

    Input: list of categories
    Returns: dataframe of all the Magic Eden listings for each category
    """

    def chunks(lst: list, n: int) -> list:
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    dfs = []  # list to hold dataframes

    for category_chunk in chunks(
        list_of_categories, 25
    ):  # iterate through the list of categories in chunks of 25
        categories_string = ",".join(
            category_chunk
        )  # convert the list of categories to a string
        url = API_URL + f"/v2/arb/me-listings?categories={categories_string}"
        r = requests.get(url)
        json_object = r.json()
        df = pd.DataFrame(json_object)

        # Sort by 'me_price' and drop duplicates based on 'category'
        df.sort_values('me_price', inplace=True)
        df.drop_duplicates(subset='category', keep='first', inplace=True)

        dfs.append(df)

    result = pd.concat(dfs, ignore_index=True)
    return result


def get_time() -> str:
    """
    Returns the current time in the format: [DD/MM/YYYY  HH:MM:SS]

    Input: None
    Returns: current time in the format: [DD/MM/YYYY  HH:MM:SS]
    """
    now = datetime.now()
    date_format = now.strftime("[%d/%m/%Y  %H:%M:%S]")
    return date_format


def join_and_calculate_profit(
    min_prices_df: pd.DataFrame, bids_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Merges the two dataframes and calculates the expected profit

    Input: dataframe of all the Magic Eden listings for each category, dataframe of all the best bids for each category
    Returns: merged dataframe with the expected profit column

    """

    # Merge the two dataframes on the 'category' column
    merged_df = pd.merge(min_prices_df, bids_df, on="category", how="inner")

    # Calculate the expected profit
    merged_df["expected_profit"] = merged_df["sol_price"] - merged_df["me_price"]

    # Add the timestamp column
    merged_df["timestamp"] = datetime.now()

    return merged_df


def dataframe_prettify(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prettifies the dataframe and returns it

    Input: dataframe
    Returns: prettified dataframe
    """
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


def run_arbs_parse() -> pd.DataFrame:
    """
    Runs the arbs_parse.py script and updates the data, then saves it to a csv file

    Input: None
    Returns: dataframe
    """

    bids_df = get_all_arbs()
    category_list = get_arbs_list(bids_df)
    min_prices_df = get_all_me_listings(category_list)
    df = join_and_calculate_profit(min_prices_df, bids_df)
    df.to_csv("data/best_bids_with_me.csv", index=False)
    print_out_dim("Data updated.")
    return df


def display_data_tabulate():
    """
    Displays the data in a table using tabulate, reads the data from the csv file

    Input: None
    Returns: None
    """

    try:
        df = pd.read_csv("data/best_bids_with_me.csv")  # If file exists, read it
    except FileNotFoundError:
        print_out_dim(
            "No data found. Updating..."
        )  # If file doesn't exist, update the data and create it
        run_arbs_parse()
        df = pd.read_csv("data/best_bids_with_me.csv")
    
    last_updated = df["timestamp"].iloc[0]  # Check when the data was updated
    last_updated = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S.%f")
    if last_updated < datetime.now() - timedelta(
        minutes=20
    ):  # if last_updated more than 20 minutes ago, run_arbs_parse()
        print_out_dim("Data is more than 20 minutes old. Updating...")
        print_out_dim("This will take ~5 seconds.")
        run_arbs_parse()
        df = pd.read_csv("data/best_bids_with_me.csv")
        last_updated = df["timestamp"].iloc[0]

    # Clear console
    os.system('cls' if os.name == 'nt' else 'clear')

    df_pretty = dataframe_prettify(df)

    # Create a table
    table = Table(show_header=True, header_style="bold magenta")
    for col in df_pretty.columns:
        table.add_column(col)

    # Add rows to the table
    for _, row in df_pretty.iterrows():
        row_as_str = row.apply(str).tolist()
        table.add_row(*row_as_str)

    console.print(table)

    print_out_dim(f"Last updated: {last_updated}")
    return df


def check_for_positives(df: pd.DataFrame):
    """
    Checks if there are any positive arbs, if there are, open the browser to the Solana Name Service page

    Input: dataframe
    Returns: None
    """
    if df["expected_profit"].max() > 0:
        print_out_dim("Positive arbs found")
        name = df["Domain Name"].iloc[0]
        url = "https://sns.id/search?search=" + name.strip()
        webbrowser.open(url)
    else:
        print_out_dim("No positive arbs found")


def print_out_dim(text: str):
    """
    Prints out the text in dim style

    Input: text
    Returns: None
    """

    print(f"{Style.DIM}{get_time()} {text}.{Style.RESET_ALL}")


def init_message():
    """
    Prints out the init message

    Input: None
    Returns: None
    """

    print(
        f" \n{Fore.BLUE}{Style.BRIGHT}BONFIDA ARBS CLI BOT{Style.RESET_ALL}\n \nGithub: Taequn\nTwitter: @candyflipline\nTelegram: @candyflipline\n"
    )


if __name__ == "__main__":
    # bids_df = get_all_arbs()
    # category_list = get_arbs_list(bids_df)
    # min_prices_df = get_all_me_listings(category_list)
    # print(min_prices_df)
    # df = join_and_calculate_profit(min_prices_df, bids_df)
    display_data_tabulate()
