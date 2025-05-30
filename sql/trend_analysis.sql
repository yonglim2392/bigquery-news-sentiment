-- 월별 감성 점수 평균 추이
SELECT
  FORMAT_DATE('%Y-%m', date) AS month,
  AVG(average_sentiment_score) AS avg_sentiment
FROM `your_project.your_dataset.daily_sentiment`
GROUP BY month
ORDER BY month;

-- 월별 PM2.5 평균 추이
SELECT
  FORMAT_DATE('%Y-%m', date) AS month,
  AVG(avg_pm25) AS avg_pm25
FROM `your_project.your_dataset.daily_pm25`
GROUP BY month
ORDER BY month;

-- 주간 변화율 (감성 점수 기준)
WITH weekly AS (
  SELECT
    DATE_TRUNC(date, WEEK(MONDAY)) AS week_start,
    AVG(average_sentiment_score) AS avg_sentiment
  FROM `your_project.your_dataset.daily_sentiment`
  GROUP BY week_start
)
SELECT
  week_start,
  avg_sentiment,
  LAG(avg_sentiment) OVER (ORDER BY week_start) AS prev_week,
  SAFE_DIVIDE(avg_sentiment - LAG(avg_sentiment) OVER (ORDER BY week_start), LAG(avg_sentiment) OVER (ORDER BY week_start)) AS sentiment_change_ratio
FROM weekly;
