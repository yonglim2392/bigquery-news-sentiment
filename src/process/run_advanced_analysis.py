import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests


def lag_correlation_analysis(df: pd.DataFrame, max_lag: int = 7):
    """
    PM2.5와 뉴스 감성 점수 간의 지연(lag) 상관관계 분석
    - max_lag: 최대 며칠까지 지연 시점 확인
    - df은 'date', 'pm25', 'sentiment' 컬럼 포함 가정
    """
    results = []
    for lag in range(max_lag + 1):
        shifted_sentiment = df['sentiment'].shift(lag)
        corr = df['pm25'].corr(shifted_sentiment)
        results.append({'lag_days': lag, 'correlation': corr})
    return pd.DataFrame(results)


def granger_causality_analysis(df: pd.DataFrame, maxlag: int = 7):
    """
    Granger 인과성 검사
    - df은 'pm25'와 'sentiment' 컬럼 포함 데이터프레임
    - 최대 lag는 maxlag
    - 결과는 p-value를 모아 데이터프레임으로 반환
    """
    test_result = {}
    for lag in range(1, maxlag + 1):
        try:
            test = grangercausalitytests(df[['pm25', 'sentiment']], maxlag=lag)
            # test[lag][0]['ssr_ftest'] 결과에서 p-value 추출
            p_value = test[lag][0]['ssr_ftest'][1]
            test_result[lag] = p_value
        except Exception as e:
            test_result[lag] = np.nan

    result_df = pd.DataFrame({
        'lag': list(test_result.keys()),
        'p_value': list(test_result.values())
    })
    return result_df


def analyze_sentiment_change_events(df: pd.DataFrame, threshold: float = 0.5):
    """
    감성 점수 급격한 변화 이벤트 탐지
    - threshold: 하루 감성 점수 차이 임계값
    - df: 날짜순 정렬, 'date'와 'sentiment_score' 컬럼 필요
    - 결과: 이벤트 날짜, 변화량, 상승/하락 표시 포함 데이터프레임
    """
    df = df.sort_values('date').reset_index(drop=True)
    df['sentiment_diff'] = df['sentiment'].diff()

    events = df.loc[abs(df['sentiment_diff']) > threshold, ['date', 'sentiment_diff']].copy()
    events['event_type'] = events['sentiment_diff'].apply(lambda x: 'increase' if x > 0 else 'decrease')
    return events


def run_advanced_analysis(df: pd.DataFrame):
    """
    df: 'date', 'pm25', 'sentiment_score' 최소 컬럼 필요
    세 가지 심화 분석 수행 후 결과 반환
    """
    lag_corr_df = lag_correlation_analysis(df)
    granger_result_df = granger_causality_analysis(df)
    events_analysis_df = analyze_sentiment_change_events(df)

    return lag_corr_df, granger_result_df, events_analysis_df
