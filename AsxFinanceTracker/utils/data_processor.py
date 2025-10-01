import pandas as pd
import numpy as np

def calculate_composite_score(df):
    """Calculate composite score based on stable growth (60%) and total growth (40%)"""
    if df.empty:
        return df

    # Normalize values between 0 and 1
    def normalize(series):
        min_val = series.min()
        max_val = series.max()
        if max_val == min_val:
            return series * 0
        return (series - min_val) / (max_val - min_val)

    # Stable Growth Score (60%)
    # This considers the consistency and sustainability of growth
    stable_growth_score = (
        (1 - normalize(df['Volatility'])) * 0.3 +          # Lower volatility (more stable)
        normalize(df['5Y Avg Dividend Yield (%)']) * 0.2 +  # Consistent income
        (1 - normalize(df['Current Price/Book Value'])) * 0.1  # Lower P/B ratio is better
    )

    # Total Growth Score (40%)
    # This considers the overall return performance
    total_growth_score = normalize(df['5Y Return Rate (%)'])

    # Combine scores with weights
    composite_score = (stable_growth_score * 0.6) + (total_growth_score * 0.4)

    # Penalize negative growth more heavily
    negative_growth_mask = df['5Y Return Rate (%)'] < 0
    composite_score[negative_growth_mask] *= 0.5

    return composite_score

def process_stock_data(df):
    """Process and clean stock data"""
    if df is None or df.empty:
        return pd.DataFrame()

    # Calculate composite score
    df['Composite Score'] = calculate_composite_score(df)

    # Sort by composite score
    df = df.sort_values('Composite Score', ascending=False)

    # Format numbers
    df['Current Price'] = df['Current Price'].round(2)
    df['5Y Return Rate (%)'] = df['5Y Return Rate (%)'].round(2)
    df['Market Cap'] = df['Market Cap'].apply(lambda x: f"${x:,.0f}")
    df['Volume'] = df['Volume'].apply(lambda x: f"{x:,.0f}")
    df['PE Ratio'] = df['PE Ratio'].round(2)
    df['5Y Avg Dividend Yield (%)'] = df['5Y Avg Dividend Yield (%)'].round(2)
    df['Current Price/Book Value'] = df['Current Price/Book Value'].round(2)
    df['Composite Score'] = df['Composite Score'].round(4)

    return df

def prepare_download_data(df):
    """Prepare data for CSV download"""
    download_df = df.copy()
    download_df.drop('Historical Data', axis=1, inplace=True)
    return download_df