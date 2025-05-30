import pandas as pd
from typing import List, Dict

def aggregate_pm25(pm25_data: List[Dict]) -> pd.DataFrame:
    """
    OpenAQ에서 가져온 PM2.5 일별 평균 정리
    """
    records = []
    for item in pm25_data:
        date = item.get('period')['datetimeTo']['utc'][:10]
        value = item.get("value", None)
        if date and value is not None:
            records.append({"date": date, "pm25": value})

    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame(columns=["date", "pm25"])

    df_grouped = df.groupby("date")["pm25"].mean().reset_index()
    return df_grouped


def merge_pm25_sentiment(
    df_pm25: pd.DataFrame, df_sentiment: pd.DataFrame
) -> pd.DataFrame:
    """
    PM2.5와 감성 점수를 날짜 기준으로 병합
    """
    df = pd.merge(df_pm25, df_sentiment, on="date", how="inner")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df