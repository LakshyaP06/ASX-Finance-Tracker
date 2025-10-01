import streamlit as st
import pandas as pd
from utils.data_fetcher import fetch_all_stocks_data
from utils.data_processor import process_stock_data, prepare_download_data
from utils.visualizer import create_stock_price_chart, create_return_rate_comparison

# Page config
st.set_page_config(page_title=" ETF ASX Stock Analysis Dashboard",
                   page_icon="📈",
                   layout="wide")

# Title and description section only
st.title("📈 ETF ASX Stock Analysis Dashboard")
st.markdown("""
This dashboard provides analysis of ASX-listed stocks, including return rates, 
price charts, and key financial metrics. Stocks are ranked using a composite score:
- 70% Stable Growth (Low Volatility, Consistent Dividends, Strong Book Value)
- 30% Total Growth (5-Year Return Rate)

Data is sourced from Yahoo Finance.
""")

# Load data
with st.spinner('Fetching stock data...'):
    raw_data = fetch_all_stocks_data()
    df = process_stock_data(raw_data)

# Main dashboard
if not df.empty:
    # Metrics overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Number of Stocks", len(df))
    with col2:
        avg_return = df['5Y Return Rate (%)'].mean()
        st.metric("Average 5Y Return", f"{avg_return:.2f}%")
    with col3:
        best_performer = df.iloc[0]
        st.metric(
            "Best Performer",
            f"{best_performer['Ticker']} ({best_performer['5Y Return Rate (%)']}%)"
        )

    # Return rate comparison chart
    st.subheader("Return Rate Comparison")
    comparison_chart = create_return_rate_comparison(df)
    st.plotly_chart(comparison_chart, use_container_width=True)

    # Stock table
    st.subheader("Stock Performance Table")

    # Filter options
    min_return = float(df['5Y Return Rate (%)'].min())
    max_return = float(df['5Y Return Rate (%)'].max())

    return_range = st.slider("Filter by Return Rate (%)", min_return,
                             max_return, (min_return, max_return))

    filtered_df = df[(df['5Y Return Rate (%)'] >= return_range[0])
                     & (df['5Y Return Rate (%)'] <= return_range[1])]

    # Display table
    display_cols = [
        'Ticker', 'Company Name', 'Current Price', '5Y Return Rate (%)',
        '5Y Avg Dividend Yield (%)', 'Current Price/Book Value', 'Market Cap',
        'Volume', 'PE Ratio', 'Composite Score'
    ]
    st.dataframe(filtered_df[display_cols].style.background_gradient(
        subset=['Composite Score'], cmap='RdYlGn'),
                 use_container_width=True)

    # Download button
    download_df = prepare_download_data(filtered_df)
    st.download_button(label="Download Data as CSV",
                       data=download_df.to_csv(index=False).encode('utf-8'),
                       file_name="asx_stock_analysis.csv",
                       mime="text/csv")

    # Individual stock analysis
    st.subheader("Individual Stock Analysis")
    selected_stock = st.selectbox("Select Stock for Detailed Analysis",
                                  df['Ticker'].tolist())

    if selected_stock:
        stock_data = df[df['Ticker'] == selected_stock].iloc[0]
        hist_data = stock_data['Historical Data']

        # Stock price chart
        price_chart = create_stock_price_chart(hist_data, selected_stock)
        st.plotly_chart(price_chart, use_container_width=True)

        # Stock details
        st.markdown(f"### {stock_data['Company Name']} ({selected_stock})")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Price", f"${stock_data['Current Price']:.2f}")
        with col2:
            st.metric("5Y Return Rate", f"{stock_data['5Y Return Rate (%)']}%")
        with col3:
            st.metric("PE Ratio", stock_data['PE Ratio'])

else:
    st.error("Unable to fetch stock data. Please try again later.")

# Footer
st.markdown("---")
st.markdown("Data source: Yahoo Finance | Updated hourly")
