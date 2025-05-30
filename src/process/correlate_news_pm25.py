import pandas as pd
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns


def compute_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    PM2.5와 감성 점수 간의 상관계수(Pearson & Spearman)를 계산
    """
    if df.empty or "pm25" not in df or "sentiment" not in df:
        raise ValueError("Input DataFrame must have 'pm25' and 'sentiment' columns")

    pearson_corr, p_val_pearson = pearsonr(df["pm25"], df["sentiment"])
    spearman_corr, p_val_spearman = spearmanr(df["pm25"], df["sentiment"])

    return pd.DataFrame({
        "method": ["pearson", "spearman"],
        "correlation": [pearson_corr, spearman_corr],
        "p_value": [p_val_pearson, p_val_spearman]
    })


def plot_correlation(df: pd.DataFrame, save_path: str = "correlation_plot.png") -> None:
    """
    PM2.5 vs 감성 점수의 관계 시각화 (산점도 + 회귀선)
    """
    if df.empty:
        print("Empty DataFrame, skipping plot.")
        return

    plt.figure(figsize=(8, 6))
    sns.regplot(x="pm25", y="sentiment", data=df)
    plt.title("PM2.5 vs Sentiment Score")
    plt.xlabel("PM2.5 (daily mean)")
    plt.ylabel("Sentiment Score (daily avg)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Plot saved to {save_path}")