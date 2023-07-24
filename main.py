import streamlit as st
from utils.misc import CATEGORIES_DICTIONARY
from utils.methods import get_arbs_me_bonfida, convert_json_to_df

#change the tab title
st.set_page_config(page_title="Bonfida Arbitrage Finding Tool")
st.title("Bonfida Arbitrage Finding Tool")

st.sidebar.title("Settings")
st.sidebar.write("Choose the category you want to find arbitrage opportunities for")
# For category, select the key from the dictionary
CATEGORIES = list(CATEGORIES_DICTIONARY.keys())
category = st.sidebar.selectbox("Category", CATEGORIES)

# category = st.sidebar.selectbox("Category", CATEGORIES)
st.sidebar.write("Choose the maximum bid price")
max_bid = st.sidebar.number_input(
    "Maximum bid price", min_value=0.0, max_value=1000000.0, value=1.0, step=0.01
)

# use the methods from utils/methods.py to get the json and convert it to a dataframe
try:
    selected_category = CATEGORIES_DICTIONARY[category]  # type: ignore

    json_input = get_arbs_me_bonfida(selected_category, max_bid)  # type: ignore
    convert_json_to_df(json_input)
except Exception as e:
    st.error(e)
