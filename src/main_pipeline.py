import os
import pandas as pd
from google.cloud import bigquery

from src.fetch.fetch_news import fetch_news
from src.fetch.fetch_climate import fetch_air_quality
from src.process.sentiment_analysis import analyze_sentiments
from src.process.aggregate_daily_scores import aggregate_pm25, merge_pm25_sentiment
from src.process.correlate_news_pm25 import compute_correlations
from src.process.run_advanced_analysis import run_advanced_analysis
from src.report.report_generator import generate_advanced_html_report
from src.fetch.bq_writer import write_to_bigquery

# BigQuery client 초기화
client = bigquery.Client()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET_ID")

def load_sql_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def execute_bigquery(sql: str):
    query_job = client.query(sql)
    result = query_job.result()
    return result

def main():
    # 1. 데이터 수집
    articles = fetch_news()
    pm25_raw = fetch_air_quality()

    # 2. 전처리 및 분석
    df_pm25 = aggregate_pm25(pm25_raw)
    df_sentiment = analyze_sentiments(articles)
    df_final = merge_pm25_sentiment(df_pm25, df_sentiment)
    corr_df = compute_correlations(df_final)

    # 3. 심화 분석
    lag_corr_df, granger_result_df, events_analysis_df = run_advanced_analysis(df_final)

    # 4. BigQuery 테이블 생성 (최초 1회 실행 권장)
    create_tables_sql = load_sql_file("sql/create_tables.sql")
    execute_bigquery(create_tables_sql)
    print("BigQuery 테이블 생성 완료")

    # 5. BigQuery에 데이터 적재 (json 형식 리스트로 변환 필요)
    write_to_bigquery("news_pm25_analysis", df_final.to_dict(orient="records"))
    write_to_bigquery("lag_correlation_results", lag_corr_df.to_dict(orient="records"))
    write_to_bigquery("granger_causality_results", granger_result_df.to_dict(orient="records"))
    write_to_bigquery("events_analysis", events_analysis_df.to_dict(orient="records"))

    print("BigQuery에 데이터 업로드 완료")

    # 6. BigQuery에서 분석 쿼리 실행 (trend_analysis.sql)
    create_tables_sql = load_sql_file("sql/create_tables.sql")
    execute_bigquery(create_tables_sql)
    
    trend_sql = load_sql_file("sql/trend_analysis.sql")
    trend_result = execute_bigquery(trend_sql)

    # 결과 출력 (예: 상관계수)
    for row in trend_result:
        print(f"최근 30일 PM2.5와 감성 점수 상관계수: {row['correlation']}")

    # 7. 시각화 및 리포트 생성
    plot_path = "results/correlation_plot.png"
    # plot_correlation 함수가 내부에서 파일 저장을 한다고 가정
    from src.process.correlate_news_pm25 import plot_correlation
    plot_correlation(df_final, save_path=plot_path)

    generate_advanced_html_report(corr_df, lag_corr_df, granger_result_df, events_analysis_df, df_final, plot_path)

    print("분석 및 리포트 생성 완료")

if __name__ == "__main__":
    main()
