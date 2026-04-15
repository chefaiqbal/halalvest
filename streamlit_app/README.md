# HalalVest - Streamlit Version

A free, open-source stock tracking bot for Islamic investing. Track halal-screened stocks, get AI-powered buy/sell/hold recommendations, and make informed investment decisions.

## 🚀 Quick Start - Deploy in 5 Minutes

### Prerequisites: Get Your Free Finnhub API Key (2 minutes)

1. **Go to [Finnhub.io](https://finnhub.io/register?plan=free)**
2. **Sign up for free account** (no credit card needed)
3. **Copy your API key** from the dashboard
4. **You're done!** The free tier gives you 60 API calls/minute (plenty for this app)

### Option 1: Deploy to Streamlit Cloud (Easiest & Free)

1. **Push this folder to GitHub**
   ```bash
   git add streamlit_app/
   git commit -m "Add HalalVest Streamlit app"
   git push origin main
   ```

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
   - Click "New app"
   - Select your GitHub repository
   - Select branch: `main`
   - File path: `streamlit_app/app.py`
   - Click "Deploy"

3. **Add your Finnhub API Key to Streamlit Secrets**
   - In Streamlit Cloud dashboard, go to app settings
   - Click "Secrets"
   - Add: `FINNHUB_API_KEY = "your_api_key_here"`
   - Save and redeploy

4. **That's it!** Your app is now live and your friend can access it from iOS Safari

### Option 2: Run Locally

```bash
cd streamlit_app

# Install dependencies
pip install -r requirements.txt

# Create or edit .streamlit/secrets.toml and add:
# FINNHUB_API_KEY = "your_finnhub_api_key_here"

# Run the app
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

---

## ✨ Features

✅ **Halal Stock Screening**
- Automatically filters S&P 500 stocks by Islamic finance principles
- Excludes prohibited sectors (alcohol, tobacco, gambling, etc.)
- Checks debt-to-equity ratios for riba concerns
- Halal compliance scoring (0-100%)

✅ **Smart Recommendations**
- Technical Analysis: SMA, RSI, MACD, Volume trends
- Fundamental Analysis: P/E ratios, earnings, ROE, profit margins
- Combined confidence scoring
- Buy/Sell/Hold signals with reasoning

✅ **Real-Time Data**
- Live stock prices (Finnhub API)
- 1 year of historical data
- Instant analysis and recommendations

✅ **Mobile-Friendly**
- Perfect for iOS Safari
- Responsive design
- Touch-friendly interface

✅ **Completely Free**
- Free hosting on Streamlit Cloud
- Free stock data from Finnhub (60 calls/min, no credit card needed)
- No hidden costs

---

## 📊 How It Works

### 1. Halal Screening
- Analyzes company sector
- Checks debt-to-equity ratio (Islamic principle)
- Compliance scoring

### 2. Technical Analysis
- **SMA (20, 50, 200)**: Identify trends
- **RSI (14)**: Identify overbought/oversold
- **MACD**: Momentum and trend
- **Volume Trend**: Confirm movements

### 3. Fundamental Analysis
- **P/E Ratio**: Valuation assessment
- **Debt-to-Equity**: Financial health
- **ROE**: Profitability efficiency
- **Profit Margins**: Operational efficiency

### 4. Recommendation Algorithm
- **Technical Score (50%)**: Market trends
- **Fundamental Score (50%)**: Company health
- **Combined Score**: Buy/Sell/Hold decision
- **Confidence Level**: How certain we are

```
Combined Score Interpretation:
- > 65: 🟢 BUY (Strong signals)
- 55-65: 💹 STRONG HOLD (Positive outlook)
- 45-55: 〰️ HOLD (Mixed signals)
- 35-45: ⚠️ WEAK HOLD (Negative outlook)
- < 35: 🔴 SELL (Weak signals)
```

---

## 📱 Pages

### 1. Dashboard
- Quick overview of halal stocks
- Your watchlist count
- Top 15 halal stocks with prices

### 2. Stock Analysis
- Search any stock symbol
- Full technical analysis
- Full fundamental analysis
- Halal compliance check
- Buy/Sell/Hold recommendation
- Add to watchlist

### 3. Halal Screening
- Browse pre-screened halal stocks
- Click any symbol for details
- See compliance score and issues

### 4. My Watchlist
- View all saved stocks
- See latest recommendations
- Quick access to analysis
- Remove stocks with one click

### 5. About
- Learn how it works
- Important disclaimers
- Data sources

---

## 📝 Important Disclaimer

⚠️ **This tool is for EDUCATIONAL PURPOSES ONLY!**

- **NOT financial advice**
- Always do your own research
- Consult with a financial advisor before investing
- Never invest based solely on this tool
- Stock market involves risk
- Past performance doesn't guarantee future results
- For Islamic finance compliance, consult with a Sharia advisor

---

## 🛠️ Tech Stack

- **Framework**: Streamlit (Python)
- **Data**: Finnhub API (free, requires free API key)
- **Technical Analysis**: TA Library
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Hosting**: Streamlit Cloud (free)

---

## 📊 Supported Halal Stocks

### Technology
NVDA, AMD, ORCL, AVGO, ADBE, CRM, INTU, SNPS, CDNS, NXPI, MSFT, GOOGL

### Healthcare
JNJ, UNH, PFE, ABBV, MRK, TMO, LLY, AZN, AMGN, GILD

### Finance
JPM, BAC, WFC, GS, MS, BLK, SCHW, CME, ICE, MSCI

### Consumer & Retail
AMZN, WMT, HD, MCD, NKE, SBUX, TJX, COST, LOW, TSCO

### Energy
XOM, CVX, COP, SLB, MPC, PSX, VLO, FANG, EOG, MUR

### Industrial & Materials
BA, GE, MMM, RTX, HON, CAT, DE, FDX, UPS

### Real Estate & Utilities
NEE, DUK, SO, D, EXC, AEP, XEL, SRE, WEC

**And many more!** Total of 90+ pre-screened halal stocks.

---

## 🔍 Analysis Details

### Technical Metrics

- **SMA (Simple Moving Average)**
  - 20-day: Short-term trend
  - 50-day: Medium-term trend
  - 200-day: Long-term trend
  - Signal: When SMA 20 > SMA 50 > SMA 200 = Uptrend

- **RSI (Relative Strength Index)**
  - < 30: Oversold (potential bounce)
  - 30-70: Normal trading range
  - > 70: Overbought (potential pullback)

- **MACD (Moving Average Convergence Divergence)**
  - Positive histogram: Bullish momentum
  - Negative histogram: Bearish momentum

- **Volume Trend**
  - High volume: Strong conviction
  - Low volume: Weak conviction

### Fundamental Metrics

- **P/E Ratio (Price-to-Earnings)**
  - < 15: Undervalued
  - 15-25: Fair value
  - > 25: Premium valuation

- **Debt-to-Equity**
  - < 0.5: Very healthy
  - 0.5-1.5: Acceptable
  - > 1.5: High risk

- **ROE (Return on Equity)**
  - > 20%: Excellent profitability
  - 15-20%: Very good
  - 10-15%: Good
  - < 10%: Below average

- **Profit Margin**
  - > 20%: Outstanding
  - 10-20%: Excellent
  - 5-10%: Good
  - < 5%: Low

---

## 📞 FAQ

**Q: Is this a bot or web app?**
A: It's a web app you can access from any device, including iOS Safari. It's not a Telegram bot, but could be extended to one.

**Q: Can my friend use it on his iPhone?**
A: Yes! Just open it in Safari and it works perfectly. You can even add it to home screen for app-like experience.

**Q: Does it cost anything?**
A: Completely free! Streamlit Cloud hosting is free for public apps, and Finnhub's free tier provides 60 API calls/minute (more than enough). No credit card needed.

**Q: How accurate are the recommendations?**
A: They're based on proven technical and fundamental indicators, but they should be used as a guide, not investment advice. Always do your own research.

**Q: Can I add more stocks?**
A: Yes! Edit `HALAL_STOCKS` list in `halal_screening.py` or search any stock in the app.

**Q: How often is data updated?**
A: Real-time during market hours. Historical data is updated daily.

---

## 🚀 Deployment Status

- ✅ Development: Complete
- ✅ Local Testing: Ready
- ⏳ Streamlit Cloud: Ready to deploy (see Quick Start)
- ✅ Mobile: iOS Safari compatible
- ✅ Data: Finnhub API integration (reliable, 60 calls/min free)

---

## 📈 Roadmap

- [ ] Portfolio tracking
- [ ] Price alerts
- [ ] Email notifications
- [ ] Advanced charting
- [ ] More technical indicators
- [ ] Zakat calculations
- [ ] Community watchlists

---

## ⚖️ License

MIT License - Feel free to use and modify

---

## 📧 Support

For issues:
1. Check the About page for more info
2. Review the analysis details above
3. Check your internet connection
4. Try refreshing the page

---

Built with ❤️ for the Islamic investing community

