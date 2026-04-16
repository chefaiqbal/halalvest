import requests
symbol="AAPL"
FMP_API_KEY = "put something"
bs_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?limit=1&apikey=demo"
print(requests.get(bs_url).json())
