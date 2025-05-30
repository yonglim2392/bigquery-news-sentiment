from textblob import TextBlob
import pandas as pd
from typing import List, Dict

def score_sentiment(text: str) -> float:
    try:
        return TextBlob(text).sentiment.polarity
    except Exception:
        return 0.0

def analyze_sentiments(articles: List[Dict]) -> pd.DataFrame:
    results = []
    for article in articles:
        date = article.get("publishedAt", "")[:10]
        title = article.get("title", "")
        desc = article.get("description", "")
        text = f"{title} {desc}".strip()

        if not date or not text:
            continue

        sentiment = score_sentiment(text)
        results.append({"date": date, "score": sentiment})

    df = pd.DataFrame(results)
    if df.empty:
        return pd.DataFrame(columns=["date", "sentiment"])

    df_grouped = df.groupby("date")["score"].mean().reset_index()
    df_grouped.rename(columns={"score": "sentiment"}, inplace=True)
    return df_grouped