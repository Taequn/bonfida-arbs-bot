import pytest
import requests
import pandas as pd
from unittest.mock import Mock, patch

from utils.methods import get_all_arbs, get_arbs_me_bonfida, get_min_price_me_category
from utils.endpoints import API_URL


@patch("requests.get")
@patch("pandas.DataFrame.to_csv")
def test_get_all_arbs(mock_to_csv, mock_get):
    # Mock the response from the API
    mock_response = Mock()
    mock_get.return_value = mock_response
    # {'0x99-club': {'nb_domains': 1, 'sol_price': 0.01}, 'countries': {'nb_domains': 1, 'sol_price': 0.7}, '3-letters': {'nb_domains': 1, 'sol_price': 0.712}, '999-club': {'nb_domains': 2, 'sol_price': 16.2}, '4-letter-dictionary': {'nb_domains': 7, 'sol_price': 1.0}, '2-digit-palindromes': {'nb_domains': 1, 'sol_price': 21.0}, 'spanish-nouns': {'nb_domains': 1, 'sol_price': 0.1}, '4-digit-palindromes': {'nb_domains': 1, 'sol_price': 5.6}, '0xemojis': {'nb_domains': 1, 'sol_price': 0.001}, '5-digit-palindromes': {'nb_domains': 5, 'sol_price': 0.2}, '5-letter-dictionary': {'nb_domains': 5, 'sol_price': 0.115}, '0x10k-club': {'nb_domains': 1, 'sol_price': 0.002}, '2-letters': {'nb_domains': 1, 'sol_price': 10.0}, 'english-adjectives': {'nb_domains': 2, 'sol_price': 0.1}, 'triple-emoji': {'nb_domains': 1, 'sol_price': 0.21}, 'double-emoji': {'nb_domains': 1, 'sol_price': 0.4}, 'english-nouns': {'nb_domains': 1, 'sol_price': 0.5}, 'single-emoji': {'nb_domains': 1, 'sol_price': 1.1}, '3-letter-palindromes': {'nb_domains': 2, 'sol_price': 1.0}, '99-club': {'nb_domains': 1, 'sol_price': 32.0}, '9-club': {'nb_domains': 1, 'sol_price': 120.0}, '1-letter': {'nb_domains': 1, 'sol_price': 12.5}, 'emoji-flag-club': {'nb_domains': 1, 'sol_price': 1.3}, 'surnames': {'nb_domains': 5, 'sol_price': 0.1}, '100k-club': {'nb_domains': 2, 'sol_price': 0.161}, 'months': {'nb_domains': 1, 'sol_price': 2.6}, '2-letter-palindromes': {'nb_domains': 1, 'sol_price': 0.2}, 'strobogrammatic-club': {'nb_domains': 1, 'sol_price': 0.05}, '10k-club': {'nb_domains': 1, 'sol_price': 1.41}, '0x999-club': {'nb_domains': 1, 'sol_price': 0.001}, 'english-verbs': {'nb_domains': 3, 'sol_price': 0.5}, '3-digit-palindromes': {'nb_domains': 1, 'sol_price': 17.5}, 'mnemonic-club': {'nb_domains': 2, 'sol_price': 0.371}}
    mock_response.json.return_value = {
        "category1": {"nb_domains": 1, "sol_price": 0.01},
        "category2": {"nb_domains": 2, "sol_price": 0.02},
    }

    # Call the function
    get_all_arbs()

    # Check the API was called correctly
    mock_get.assert_called_once_with(API_URL + "/v2/arb/category-best-bid")

    # Check the DataFrame was created correctly
    expected_df = pd.DataFrame(
        {
            "category1": {"nb_domains": 1.0, "sol_price": 0.01},
            "category2": {"nb_domains": 2.0, "sol_price": 0.02},
        }
    ).T
    pd.testing.assert_frame_equal(
        pd.DataFrame(mock_response.json.return_value).T, expected_df
    )

    # Check the CSV was saved correctly
    mock_to_csv.assert_called_once_with("data/best_bids.csv")

@patch('requests.get')
def test_get_arbs_me_bonfida(mock_get):
    # Mock the response from the API
    mock_response = Mock()
    mock_get.return_value = mock_response
    mock_response.json.return_value = [
        {'domain_name': 'external', 'expected_profit': 89988.0, 'me_price': 12.0},
        {'domain_name': 'texture', 'expected_profit': 89997.0, 'me_price': 3.0},
    ]

    # Call the function
    df = get_arbs_me_bonfida("test_category", 9000)

    # Check the API was called correctly
    mock_get.assert_called_once_with(API_URL + "/v2/arb/me-bonfida?category=test_category&max_bid=9000")

    # Check the DataFrame was created correctly
    expected_df = pd.DataFrame(mock_response.json.return_value)
    pd.testing.assert_frame_equal(df, expected_df)

@patch('utils.methods.get_arbs_me_bonfida')
def test_get_min_price_me_category(mock_get_arbs_me_bonfida):
    # Mock the DataFrame returned by the get_arbs_me_bonfida function
    mock_get_arbs_me_bonfida.return_value = pd.DataFrame([
        {'domain_name': 'external', 'expected_profit': 89988.0, 'me_price': 12.0},
        {'domain_name': 'texture', 'expected_profit': 89997.0, 'me_price': 3.0},
    ])

    # Call the function
    series = get_min_price_me_category("test_category")

    # Check the get_arbs_me_bonfida function was called correctly
    mock_get_arbs_me_bonfida.assert_called_once_with("test_category", 90000)

    # Check the returned DataFrame has the correct data
    expected_series = pd.Series({
        'domain_name': 'texture', 
        'expected_profit': 89997.0, 
        'me_price': 3.0, 
        'category': 'test_category'
    }, name=1)
    pd.testing.assert_series_equal(series, expected_series)

