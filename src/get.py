import requests

GUARDIAN_API_URL = "https://content.guardianapis.com/search"


def fetch_guardian_articles(guardian_api_key, query, date_from):
    """Contacts the Guardian API and retrieves the ten most recent
    articles which relate to the query specified in the input"""

    params = {
        "q": query,
        "api-key": guardian_api_key,
        "order-by": "newest",
        "page-size": 10,
    }
    if date_from:
        params["from-date"] = date_from

    response = requests.get(GUARDIAN_API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    articles = [
        {
            "webPublicationDate": item["webPublicationDate"],
            "webTitle": item["webTitle"],
            "webUrl": item["webUrl"],
        }
        for item in data["response"]["results"]
    ]

    return articles
