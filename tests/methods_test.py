import pytest
import requests
import pandas as pd
from unittest.mock import patch, Mock
from utils.methods import (
    get_all_arbs,
    get_arbs_list,
    get_all_me_listings,
    join_and_calculate_profit,
    get_time,
)


@patch("requests.get")
def test_get_all_arbs(mock_get):
    mock_response = Mock()
    expected_dict = {
        "cat1": {"nb_domains": 1, "sol_price": 100},
        "cat2": {"nb_domains": 2, "sol_price": 200},
    }
    mock_response.json.return_value = expected_dict
    mock_get.return_value = mock_response

    df = get_all_arbs()

    # assertions to check if the function behaves as expected
    assert not df.empty
    assert set(df.columns) == {"category", "nb_domains", "sol_price"}
    assert len(df) == len(expected_dict)
    assert df["category"].tolist() == list(expected_dict.keys())
    assert df["nb_domains"].tolist() == [1, 2]
    assert df["sol_price"].tolist() == [100, 200]


def test_get_arbs_list():
    df = pd.DataFrame(
        {
            "category": ["a", "b", "c"],
            "nb_domains": [1, 2, 3],
            "sol_price": [1.0, 2.0, 3.0],
        }
    )
    assert get_arbs_list(df) == ["a", "b", "c"]


@patch("requests.get")
def test_get_all_me_listings(mock_get):
    mock_response = Mock()
    expected_dict = {
        "domain_name": ["a", "b"],
        "me_price": [1.0, 2.0],
        "category": ["a", "b"],
    }
    mock_response.json.return_value = expected_dict
    mock_get.return_value = mock_response

    df = get_all_me_listings(["a", "b"])

    assert not df.empty
    assert set(df.columns) == {"category", "me_price", "domain_name"}
    assert len(df) == len(expected_dict["domain_name"])


def test_join_and_calculate_profit():
    df1 = pd.DataFrame({"category": ["a", "b"], "me_price": [1.0, 2.0]})
    df2 = pd.DataFrame(
        {"category": ["a", "b"], "nb_domains": [1, 2], "sol_price": [1.5, 2.5]}
    )
    df = join_and_calculate_profit(df1, df2)

    assert not df.empty
    assert set(df.columns) == {
        "category",
        "me_price",
        "nb_domains",
        "sol_price",
        "expected_profit",
        "timestamp",
    }
    assert df["expected_profit"].tolist() == [0.5, 0.5]


@patch("utils.methods.datetime")
def test_get_time(mock_datetime):
    mock_datetime.now.return_value.strftime.return_value = "[01/01/2020  12:00:00]"
    assert get_time() == "[01/01/2020  12:00:00]"
