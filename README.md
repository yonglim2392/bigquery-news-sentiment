# 🌤️ Climate & News Data Platform Pipeline

**기상 및 대기질 데이터와 뉴스 감성 데이터를 통합 분석하여 사회 반응 및 기후 트렌드를 자동화된 빅쿼리 기반 데이터 파이프라인으로 구축하는 프로젝트입니다.**

## 🔍 프로젝트 개요

- 실시간 뉴스와 미세먼지 데이터를 수집
- 뉴스 감성 점수 산출 및 미세먼지 농도와의 상관분석
- 시차(lag)를 고려한 심층 통계 분석 (Granger 인과성, 이벤트 분석)
- 분석 결과를 BigQuery에 저장 및 Airflow 기반 워크플로우 자동화 (추후 확장)
- HTML 리포트 자동 생성 및 시각화 제공

## 🛠 사용 기술

- **언어/라이브러리**: Python, pandas, NumPy, statsmodels, Jinja2
- **데이터 플랫폼**: Google BigQuery (빅쿼리)
- **시각화**: matplotlib, seaborn
- **기상/대기 데이터**: OpenAQ API, 공공 데이터 활용
- **뉴스 데이터**: 뉴스 API, RSS 크롤링

## 🚀 실행 방법

1. BigQuery 프로젝트 및 데이터셋 생성  
   - `sql/create_tables.sql` 을 BigQuery에서 실행해 테이블을 생성합니다.

2. Python 환경 설정  
```bash
pip install -r requirements.txt
```

3. src/config.py에 Google Cloud 인증 및 프로젝트 정보 설정

4. 전체 파이프라인 실행
```bash
python src/main_pipeline.py
```

## ✅ 주요 기능 설명
- 뉴스 기사 실시간 수집 및 본문 감성 분석
- 공공 대기질 데이터(PM2.5 등) 수집 및 일별 집계
- 뉴스 감성 점수와 미세먼지 농도 간 상관관계 분석 및 시차(Lag) 분석
- Granger 인과성 분석과 주요 이벤트 분석 포함 심층 통계분석
- 결과 자동 시각화 및 HTML 리포트 생성
- BigQuery 적재를 통한 데이터 플랫폼 구현

## 📈 향후 개선 방향
- 추가 기상 변수 및 다중 지역 확장
- BigQuery ML을 활용한 예측 모델 개발
- 사용자 대시보드(예: Data Studio) 연동

## 🧾 라이선스

본 프로젝트는 MIT 라이선스를 따릅니다.