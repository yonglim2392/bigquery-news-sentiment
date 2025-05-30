import pandas as pd
from jinja2 import Template
import base64
import os


def encode_image_base64(image_path: str) -> str:
    """이미지를 base64로 인코딩해 HTML에 포함"""
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def generate_result_explanations(corr_df, lag_corr_df, granger_df, sentiment_events_df):
    """분석 결과 데이터프레임을 기반으로 자동 해석 텍스트 생성"""

    explanations = {}

    # 1. 기본 상관분석 결과 해석
    corr_val = corr_df['correlation'].iloc[0]
    explanations['basic_correlation'] = (
        f"상관계수는 두 변수 간 연관성 정도를 나타냅니다. 본 데이터에서 상관계수는 약 {corr_val:.2f}로, "
        f"미세먼지 농도가 높아질수록 뉴스의 부정적 감성이 다소 증가하는 경향을 보입니다. "
        f"이는 미세먼지 악화가 뉴스 감성에 영향을 줄 수 있음을 의미합니다. "
        f"하지만 1에 가까운 강한 관계는 아니므로 다른 요인들도 감성에 영향을 미친다고 볼 수 있습니다."
    )

    # 2. 지연 상관관계 해석
    if not lag_corr_df.empty:
        max_lag_row = lag_corr_df.loc[lag_corr_df['correlation'].idxmax()]
        lag_days = max_lag_row['lag_days']
        lag_corr_val = max_lag_row['correlation']
        if lag_days == 0:
            explanations['lag_correlation'] = (
                f"동일한 날(0일 지연)의 상관계수가 {lag_corr_val:.2f}로 가장 높게 나타났습니다. "
                f"이는 미세먼지 농도와 뉴스 감성이 즉각적으로 연관되어 있음을 의미합니다."
            )
        else:
            explanations['lag_correlation'] = (
                f"{lag_days}일 지연 시 상관계수가 {lag_corr_val:.2f}로 가장 높게 나타났습니다. "
                f"이는 미세먼지 변화가 뉴스 감성에 영향을 미치는 데 시간이 걸릴 수 있음을 시사합니다."
            )
    else:
        explanations['lag_correlation'] = "지연 상관분석 데이터가 없습니다."

    # 3. Granger 인과성 검정 결과 해석
    if not granger_df.empty:
        p_value = granger_df['p_value'].iloc[0]
        if p_value < 0.01:
            explanations['granger_causality'] = (
                f"Granger 인과성 검정 결과 p-value가 {p_value:.4f}로 매우 낮아, "
                f"미세먼지 농도가 뉴스 감성 변화를 예측하는 데 유의미한 영향을 미친다는 증거가 있습니다. "
                f"하지만 인과성 검정은 완전한 인과 관계를 증명하지는 않으므로 해석에 주의가 필요합니다."
            )
        else:
            explanations['granger_causality'] = (
                f"Granger 인과성 검정 결과 p-value가 {p_value:.4f}로, "
                f"미세먼지 농도가 뉴스 감성 변화를 예측한다는 통계적 증거가 부족합니다."
            )
    else:
        explanations['granger_causality'] = "Granger 인과성 검정 데이터가 없습니다."

    # 4. 뉴스 감성 급격 변화 이벤트 해석
    if not sentiment_events_df.empty:
        dates = sentiment_events_df['date'].dt.strftime('%Y-%m-%d').tolist()
        explanations['sentiment_events'] = (
            f"분석 기간 동안 {', '.join(dates)} 등에 뉴스 감성 점수가 급격히 변화하였습니다. "
            f"이 기간에 미세먼지 농도 변화도 함께 확인되어, 환경 변화와 사회적 반응이 연관되어 있을 가능성을 보여줍니다."
        )
    else:
        explanations['sentiment_events'] = "감성 변화 이벤트 데이터가 없습니다."

    return explanations


def generate_advanced_html_report(
    corr_df: pd.DataFrame,
    lag_corr_df: pd.DataFrame,
    granger_df: pd.DataFrame,
    sentiment_events_df: pd.DataFrame,
    merged_df: pd.DataFrame,
    image_path: str,
    output_path: str = "results/correlation_report.html"
):
    """
    PM2.5와 뉴스 감성 상관분석 결과를 HTML로 저장하며,
    자동 해석 텍스트를 포함하여 누구나 쉽게 이해 가능하도록 함.
    """

    with open("src/report/templates/report_template.html", "r", encoding="utf-8") as f:
        template_str = f.read()

    image_base64 = encode_image_base64(image_path)
    explanations = generate_result_explanations(corr_df, lag_corr_df, granger_df, sentiment_events_df)

    template = Template(template_str)
    html = template.render(
        correlation_table=corr_df.round(3).to_html(index=False),
        lag_correlation_table=lag_corr_df.round(3).to_html(index=False),
        granger_causality_table=granger_df.round(4).to_html(index=False),
        sentiment_events_table=sentiment_events_df.to_html(index=False),
        data_preview=merged_df.head(10).round(3).to_html(index=False),
        correlation_plot=image_base64,
        explanations=explanations
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML 리포트 생성 완료: {output_path}")
