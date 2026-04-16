with open("/home/amiriqbal/halalvest/streamlit_app/charting.py", "r") as f:
    content = f.read()

# add ta import
if "import ta\n" not in content:
    content = content.replace("import pandas as pd", "import pandas as pd\nimport ta")

# fix the RSI plot
old_rsi_plot = "y=[rsi] * len(df)"
new_rsi_plot = "y=ta.momentum.RSIIndicator(df['Close'], window=14).rsi()"

content = content.replace(old_rsi_plot, new_rsi_plot)

# Add SMA traces creation dynamically since technical_analysis.calculate_sma returns a dict with last values, not dataframes
content = content.replace(
    "y=df['SMA_20']",
    "y=df['Close'].rolling(window=20).mean()"
)
content = content.replace(
    "y=df['SMA_50']",
    "y=df['Close'].rolling(window=50).mean()"
)
content = content.replace(
    "y=df['SMA_200']",
    "y=df['Close'].rolling(window=200).mean()"
)

with open("/home/amiriqbal/halalvest/streamlit_app/charting.py", "w") as f:
    f.write(content)

