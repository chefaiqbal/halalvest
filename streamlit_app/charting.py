"""
Charting utilities for technical analysis visualization
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import ta
from technical_analysis import get_historical_data, calculate_sma, calculate_rsi


def create_price_chart(symbol: str) -> go.Figure:
    """Create interactive price chart with SMA and RSI"""
    try:
        df = get_historical_data(symbol, period='6mo')

        if df.empty:
            return None

        # Calculate indicators
        sma = calculate_sma(df)
        rsi = calculate_rsi(df)

        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.15,
            row_heights=[0.7, 0.3],
            subplot_titles=(f'{symbol} Price Action', 'RSI (14)')
        )

        # Add candlestick price
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['Close'],
                mode='lines',
                name='Close Price',
                line=dict(color='#1f77b4', width=2)
            ),
            row=1, col=1
        )

        # Add SMA lines
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['Close'].rolling(window=20).mean(),
                mode='lines',
                name='SMA 20',
                line=dict(color='orange', width=1, dash='dash')
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['Close'].rolling(window=50).mean(),
                mode='lines',
                name='SMA 50',
                line=dict(color='red', width=1, dash='dash')
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['Close'].rolling(window=200).mean(),
                mode='lines',
                name='SMA 200',
                line=dict(color='green', width=1, dash='dash')
            ),
            row=1, col=1
        )

        # Add RSI
        fig.add_trace(
            go.Scatter(
                x=df.index, y=ta.momentum.RSIIndicator(df['Close'], window=14).rsi(),
                mode='lines',
                name='RSI (14)',
                line=dict(color='purple', width=2)
            ),
            row=2, col=1
        )

        # Add overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

        # Update layout
        fig.update_layout(
            title=f'{symbol} - 6 Month Technical Analysis',
            hovermode='x unified',
            height=600,
            template='plotly_white'
        )

        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="RSI", row=2, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)

        return fig
    except Exception as e:
        return None


def create_comparison_chart(symbols: list) -> go.Figure:
    """Create comparison chart for multiple stocks"""
    try:
        fig = go.Figure()

        for symbol in symbols:
            df = get_historical_data(symbol, period='3mo')
            if not df.empty:
                # Normalize to percentage change from first price
                normalized = ((df['Close'] / df['Close'].iloc[0]) - 1) * 100

                fig.add_trace(
                    go.Scatter(
                        x=df.index, y=normalized,
                        mode='lines',
                        name=symbol,
                        line=dict(width=2)
                    )
                )

        fig.update_layout(
            title='Stock Comparison - 3 Month Performance',
            xaxis_title='Date',
            yaxis_title='Performance (%)',
            hovermode='x unified',
            height=500,
            template='plotly_white'
        )

        return fig
    except Exception as e:
        return None


def create_volume_chart(symbol: str) -> go.Figure:
    """Create volume chart"""
    try:
        df = get_historical_data(symbol, period='3mo')

        if df.empty:
            return None

        fig = go.Figure()

        # Add volume bars
        colors = ['red' if df['Close'].iloc[i] < df['Open'].iloc[i] else 'green'
                  for i in range(len(df))]

        fig.add_trace(
            go.Bar(
                x=df.index, y=df['Volume'],
                name='Volume',
                marker=dict(color=colors)
            )
        )

        fig.update_layout(
            title=f'{symbol} - Volume (3 Month)',
            xaxis_title='Date',
            yaxis_title='Volume',
            height=400,
            template='plotly_white'
        )

        return fig
    except Exception as e:
        return None
