import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import time
from random import uniform


@st.cache_data(ttl=3600)
def get_asx_tickers():
    """Get list of ASX tickers"""
    try:
        with open('ETFList.txt', 'r') as file:
            # Read tickers and strip whitespace, add .AX suffix
            asx_tickers = [
                line.strip() + '.AX' for line in file if line.strip()
            ]
        return asx_tickers
    except Exception as e:
        st.error(f"Error reading ASX tickers: {str(e)}")
        return []


def fetch_with_retry(ticker, period='5y', max_retries=3, initial_delay=1):
    """Fetch data with retry mechanism"""
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            info = stock.info
            return hist, info
        except Exception as e:
            if "Too Many Requests" in str(e):
                if attempt < max_retries - 1:
                    delay = initial_delay * (2**attempt) + uniform(
                        0, 1)  # Exponential backoff with jitter
                    st.warning(
                        f"Rate limited for {ticker}. Retrying in {delay:.1f} seconds..."
                    )
                    time.sleep(delay)
                    continue
            st.error(f"Error fetching data for {ticker}: {str(e)}")
            return None, None
    return None, None


@st.cache_data(ttl=3600)
def fetch_stock_data(ticker, period='5y'):
    """Fetch stock data for a given ticker"""
    return fetch_with_retry(ticker, period)


def calculate_volatility(hist_data):
    """Calculate stock volatility using standard deviation of returns"""
    returns = hist_data['Close'].pct_change(fill_method=None)
    return returns.std() * (252**0.5)  # Annualized volatility


@st.cache_data(ttl=3600)
def fetch_all_stocks_data():
    """Fetch data for all ASX stocks"""
    tickers = get_asx_tickers()
    all_data = []
    total_tickers = len(tickers)

    for idx, ticker in enumerate(tickers, 1):
        st.text(f"Processing {ticker} ({idx}/{total_tickers})")
        hist, info = fetch_stock_data(ticker)
        if hist is not None and not hist.empty:
            try:
                start_price = hist['Close'].iloc[0]
                current_price = hist['Close'].iloc[-1]
                return_rate = (
                    (current_price - start_price) / start_price) * 100
                volatility = calculate_volatility(hist)

                # Get Price/Book ratio and 5Y Average Dividend Yield
                price_to_book = info.get('priceToBook', 0)
                five_year_div_yield = info.get('fiveYearAvgDividendYield', 0)

                # Only include if we have valid metrics
                if price_to_book > 0 or five_year_div_yield > 0:
                    stock_data = {
                        'Ticker':
                        ticker,
                        'Company Name':
                        info.get('longName', ticker.replace('.AX', '')),
                        'Current Price':
                        current_price,
                        '5Y Return Rate (%)':
                        return_rate,
                        'Market Cap':
                        info.get('marketCap', 0),
                        'Volume':
                        info.get('volume', 0),
                        'PE Ratio':
                        info.get('trailingPE', 0),
                        '5Y Avg Dividend Yield (%)':
                        five_year_div_yield,
                        'Current Price/Book Value':
                        price_to_book,
                        'Volatility':
                        volatility,
                        'Historical Data':
                        hist
                    }
                    all_data.append(stock_data)
            except Exception as e:
                st.error(f"Error processing data for {ticker}: {str(e)}")
                continue

    return pd.DataFrame(all_data)
