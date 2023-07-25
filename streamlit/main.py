import streamlit as st
import pandas as pd
from utils.constants import CATEGORIES_DICTIONARY, CATEGORIES_DICTIONARY_INVERTED
from utils.methods import run_arbs_parse, dataframe_prettify
from utils.websocket_connection import websocket_run
import asyncio
from datetime import datetime

st.set_page_config(page_title="Bonfida Arb Opportunities", page_icon=":moneybag:")


def load_data():
    df = pd.read_csv("data/best_bids_with_me.csv")
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

st.sidebar.title("Options")
st.sidebar.markdown("Press the button to get online updates.")
connect = st.sidebar.button("Connect to websocket")
if connect:
    st.sidebar.text(f"Connected to websocket at\n {datetime.now()}")
    asyncio.run(websocket_run())


st.sidebar.markdown("Press the button to update the data without online connection.")
st.sidebar.button("Update Data", on_click=run_arbs_parse)
st.sidebar.text(f'Updated last time:\n{df.iloc[0]["timestamp"]}')
