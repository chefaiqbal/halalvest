import re

with open("/home/amiriqbal/halalvest/streamlit_app/finnhub_client.py", 'r') as f:
    content = f.read()

# add import yfinance correctly
if "import yfinance as yf" not in content:
    content = content.replace("import requests", "import requests\nimport yfinance as yf")

new_func = """@st.cache_data(ttl=3600, show_spinner=False)
def get_historical_data(symbol: str, resolution: str = 'D', count: int = 260) -> Optional[pd.DataFrame]:
    \"\"\"
    Get historical candlestick data using yfinance (Finnhub Free blocks /stock/candle)
    \"\"\"
    try:
        symbol = symbol.strip().upper()
        # Convert daily count to rough period equivalent for yfinance.
        period = '1y'
        if count <= 5: period = '5d'
        elif count <= 21: period = '1mo'
        elif count <= 63: period = '3mo'
        elif count <= 126: period = '6mo'
        elif count <= 504: period = '2y'
        elif count <= 1260: period = '5y'
        
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        
        if df.empty:
            return pd.DataFrame()
            
        # Standardize expected columns
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
        df.index.name = 'Date'
        if df.index.tz is not None:
            df.index = df.index.tz_convert(None)
            
        df = df.tail(count)
        return df
    except Exception as e:
        logger.error(f"Error fetching historical data: {e}")
        return pd.DataFrame()"""

# Replace the old function. Identify start and end.
pattern = r"@st\.cache_data\(ttl=3600, show_spinner=False\)\ndef get_historical_data.*?return df(?:\s*except Exception as e:\s*return pd\.DataFrame\(\))?"
# Wait, let's just do a simpler replacement.
start_idx = content.find("@st.cache_data(ttl=3600, show_spinner=False)\ndef get_historical_data")
end_idx = content.find("def get_company_news", start_idx)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_func + "\n\n\n" + content[end_idx:]
    with open("/home/amiriqbal/halalvest/streamlit_app/finnhub_client.py", 'w') as f:
        f.write(content)
    print("Replaced!")
else:
    print("Could not find bounds.")

