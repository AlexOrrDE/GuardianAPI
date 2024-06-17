from unittest.mock import patch
from src.get import fetch_guardian_articles
from mock_request import mocked_requests_get

GUARDIAN_API_URL = "https://content.guardianapis.com/search"


@patch("requests.get", side_effect=mocked_requests_get)
def test_fetch_guardian_articles(mock_get):
    guardian_api_key = "test_key"
    query = "machine learning"
    date_from = "2023-01-01"

    articles = fetch_guardian_articles(guardian_api_key, query, date_from)

    assert len(articles) == 2
    assert articles[0]["webTitle"] == "Test Article 1"
    assert articles[1]["webTitle"] == "Test Article 2"
    assert mock_get.called
    assert mock_get.call_args[0][0] == GUARDIAN_API_URL
