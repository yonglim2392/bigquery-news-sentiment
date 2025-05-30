import requests
from datetime import datetime, timedelta
from ..config import GOOGLE_NEWS_URL, GOOGLE_NEWS_API_KEY, CRAWL_DAYS, DATE_FORMAT,Target_keyword
from .logger import get_logger

logger = get_logger("fetch_news")

def fetch_news():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=CRAWL_DAYS)

    query = Target_keyword
    url = GOOGLE_NEWS_URL

    params = {
        "q": query,
        "from": start_date.strftime(DATE_FORMAT),
        "to": end_date.strftime(DATE_FORMAT),
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 100,
        "apiKey": GOOGLE_NEWS_API_KEY,
    }

    all_articles = []
    page = 1

    try:
        while True:
            params["page"] = page
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            if not articles:
                break

            all_articles.extend(articles)
            logger.info(f"Fetched {len(articles)} articles from page {page}")

            if len(articles) < params["pageSize"]:
                break
            page += 1

    except Exception as e:
        logger.error(f"Error fetching news: {e}")

    return all_articles