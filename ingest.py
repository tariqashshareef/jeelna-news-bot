"""Retrieves and saves articles on Sudan from NewsAPI."""

import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
NEWSAPI_KEY = os.environ["NEWSAPI_KEY"]

def fetch(from_date, to_date):
    """
    Fetches articles mentioning Sudan from NewsAPI for a given date range.

    Args:
        from_date: Start of date range as "YYYY-MM-DD".
        to_date: End of date range as "YYYY-MM-DD".

    Returns:
        A list of article dicts.

    Raises:
        Exception: If NewsAPI reports an error.
    """

    params = {
        "q": 'sudan NOT "south sudan" NOT "gurung"',
        "searchIn": "title,description",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,
        "from": str(from_date),
        "to": str(to_date),
        "apiKey": NEWSAPI_KEY,
    }

    response = requests.get("https://newsapi.org/v2/everything", params=params, timeout=30)

    data = response.json()

    if data["status"] != "ok":
        raise Exception(data.get("message"))
    
    return data["articles"]

def save_raw(articles, path):
    """Saves a list of article dicts to a JSON file."""
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)