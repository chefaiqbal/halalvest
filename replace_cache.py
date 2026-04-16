import re

with open("/home/amiriqbal/halalvest/streamlit_app/finnhub_client.py", "r") as f:
    content = f.read()

# Add a backup mechanism for yfinance using time.sleep backoff
new_func = """@st.cache_data(ttl=3600, show_spinner=False)
def get_historical_data(symbol: str, resolution: str = 'D', count: int = 260) -> Optional[pd.DataFrame]:
    \"\"\"
    Get historical candlestick data using yfinance (Finnhub Free blocks /stock/candle).
    Includes multiple retry mechanisms if Yahoo Finance rate limits it.
    \"\"\"
    symbol = symbol.strip().upper()
    period = '1y'
    if count <= 5: period = '5d'
    elif count <= 21: period = '1mo'
    elif count <= 63: period = '3mo'
    elif count <= 126: period = '6mo'
    elif count <= 504: period = '2y'
    elif count <= 1260: period = '5y'
    
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, auto_adjust=True, back_adjust=False)
            
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
            err_msg = str(e).lower()
            if "too many requests" in err_msg or "rate limit" in err_msg:
                logger.warning(f"⚠️ Yahoo Finance Rate Limit on attempt {attempt+1}/{max_retries}. Sleeping for {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                logger.error(f"Error fetching historical data: {e}")
                return pd.DataFrame()
                
    logger.error("❌ Exhausted retries for Yahoo Finance historical data.")
    return pd.DataFrame()"""

# Replace the old function block
start_idx = content.find("@st.cache_data(ttl=3600, show_spinner=False)\ndef get_historical_data")
end_idx = content.find("def get_company_news", start_idx)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_func + "\n\n\n" + content[end_idx:]
    with open("/home/amiriqbal/halalvest/streamlit_app/finnhub_client.py", 'w') as f:
        f.write(content)
else:
    print("Could not find block.")

