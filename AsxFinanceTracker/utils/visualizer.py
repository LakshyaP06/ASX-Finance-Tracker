import plotly.graph_objects as go
import plotly.express as px

def create_stock_price_chart(hist_data, ticker):
    """Create an interactive stock price chart"""
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=hist_data.index,
        open=hist_data['Open'],
        high=hist_data['High'],
        low=hist_data['Low'],
        close=hist_data['Close'],
        name='OHLC'
    ))

    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['Close'].rolling(window=20).mean(),
        name='20 Day MA',
        line=dict(color='orange')
    ))

    fig.update_layout(
        title=f'{ticker} Stock Price (5 Year)',
        yaxis_title='Price',
        xaxis_title='Date',
        template='plotly_white',
        height=600
    )

    return fig

def create_return_rate_comparison(df):
    """Create a bar chart comparing return rates"""
    fig = px.bar(
        df,
        x='Ticker',
        y='5Y Return Rate (%)',
        title='5-Year Return Rate Comparison',
        color='5Y Return Rate (%)',
        color_continuous_scale='RdYlGn'
    )

    fig.update_layout(
        xaxis_title='Stock Ticker',
        yaxis_title='Return Rate (%)',
        template='plotly_white',
        height=400
    )

    return fig