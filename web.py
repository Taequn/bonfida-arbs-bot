import streamlit as st
import pandas as pd
import asyncio
from datetime import datetime
from utils.methods import run_arbs_parse, dataframe_prettify
from datetime import datetime, timedelta

st.set_page_config(page_title="Bonfida Arb Opportunities", page_icon=":moneybag:")

def load_data() -> pd.DataFrame:
    '''
    Loads the data from the csv file, or runs the arbs_parse.py script if the csv file is not found
    
    Input: None
    Returns: dataframe
    '''
    try:
        df = pd.read_csv("data/best_bids_with_me.csv")
    except FileNotFoundError:
        df = run_arbs_parse()
    
    #check if data is stale (more than 20 minutes old)
    last_updated = df["timestamp"].iloc[0]
    now = datetime.now()
    last_updated = df["timestamp"].iloc[0]  # Check when the data was updated
    last_updated = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S.%f")
    if last_updated < datetime.now() - timedelta(
        minutes=20
    ):  # if last_updated more than 20 minutes ago, run_arbs_parse()
        run_arbs_parse()
        df = pd.read_csv("data/best_bids_with_me.csv")
        last_updated = df["timestamp"].iloc[0]
    
    return df

df = load_data()
df_pretty = dataframe_prettify(df)

st.title("Bonfida Arb Opportunities")
st.markdown(
    "This app shows the best bid for each category on Bonfida. \
        It also shows the best bid on Magic Eden for each category. \
            The expected profit is calculated by subtracting the Magic Eden price from the Bonfida price. \
                The data is updated on demand."
)
st.dataframe(df_pretty, width=1000, hide_index=True)

