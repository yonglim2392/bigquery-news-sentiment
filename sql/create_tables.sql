-- 감성 점수 테이블
CREATE TABLE IF NOT EXISTS `your_project.your_dataset.daily_sentiment` (
  date DATE,
  average_sentiment_score FLOAT64
);

-- PM2.5 일별 평균
CREATE TABLE IF NOT EXISTS `your_project.your_dataset.daily_pm25` (
  date DATE,
  avg_pm25 FLOAT64
);

-- 병합 테이블
CREATE TABLE IF NOT EXISTS `your_project.your_dataset.merged_sentiment_pm25` (
  date DATE,
  avg_pm25 FLOAT64,
  average_sentiment_score FLOAT64
);

-- 상관계수 결과
CREATE TABLE IF NOT EXISTS `your_project.your_dataset.correlation_results` (
  metric STRING,
  correlation_coefficient FLOAT64,
  correlation_pvalue FLOAT64,
);

-- 시차 상관 분석
CREATE TABLE IF NOT EXISTS `your_project.your_dataset.lag_correlation_results` (
  lag_days INT64,
  correlation FLOAT64
);

-- Granger 분석 결과
CREATE TABLE IF NOT EXISTS `your_project.your_dataset.granger_results` (
  lag INT64,
  p_value FLOAT64
);

-- 이벤트 영향 분석 결과
CREATE TABLE IF NOT EXISTS `your_project.your_dataset.event_impact_results` (
  event_date DATE,
  description STRING,
  avg_sentiment FLOAT64,
  avg_pm25 FLOAT64
);
