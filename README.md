# HalalVest - Halal Stock Tracker & Analyzer

A free, open-source stock tracking bot for Islamic investing. Track halal-screened stocks, get AI-powered buy/sell/hold recommendations, and make informed investment decisions with technical and fundamental analysis.

🚀 **Deploy in 5 minutes to Streamlit Cloud (completely FREE)**

## Features

✅ **Halal Stock Screening** - Automatically filters stocks by Islamic finance principles
- Excludes prohibited sectors (alcohol, tobacco, gambling, etc.)
- Checks debt-to-equity ratios for riba concerns
- Halal compliance scoring

✅ **Smart Recommendations** - AI-powered buy/sell/hold signals
- Technical Analysis: SMA, RSI, MACD, Volume trends
- Fundamental Analysis: P/E ratios, earnings, ROE, profit margins
- Combined confidence scoring

✅ **Real-Time Data** - Live stock prices and analysis
- Finnhub integration (free tier: 60 API calls/min)
- 1 year of historical data
- Instant recommendations

✅ **Mobile-Friendly** - Perfect for iOS Safari
- Works seamlessly on iPhone/iPad
- No app installation needed
- Responsive design

✅ **Completely Free** - No hidden costs
- Free hosting on Streamlit Cloud
- Free stock data from Yahoo Finance
- Open-source codebase

## Tech Stack

### Streamlit Version (Recommended - Easiest to Deploy) ⭐
- **Framework**: Streamlit (Python)
- **Data**: Finnhub API (free, requires free API key)
- **Technical Analysis**: TA Library
- **Hosting**: Streamlit Cloud (free)
- **Location**: `/streamlit_app/`

### Alternative: React + Node.js Version (Advanced)
- **Backend**: Node.js + Express
- **Frontend**: React 18 + Vite
- **Hosting**: Vercel (free)
- **Location**: `/backend/` and `/frontend/` (coming soon)

## Project Structure

```
halalvest/
├── streamlit_app/              # 🚀 STREAMLIT VERSION (Easiest!)
│   ├── app.py                      # Main Streamlit app
│   ├── halal_screening.py          # Halal stock filtering
│   ├── technical_analysis.py       # Technical indicators
│   ├── fundamental_analysis.py     # Fundamental metrics
│   ├── recommendation_engine.py    # Buy/Sell/Hold logic
│   ├── requirements.txt            # Python dependencies
│   ├── .streamlit/
│   │   └── config.toml             # Streamlit configuration
│   └── README.md                   # Deployment instructions
│
├── backend/                    # (Advanced) Express API
│   └── (Coming soon for advanced use cases)
│
├── frontend/                   # (Advanced) React web app
│   └── (Coming soon for advanced use cases)
│
└── README.md                   # This file
```

## 🚀 Quick Start (Choose One)

### ✨ OPTION 1: Deploy to Streamlit Cloud in 5 Minutes (EASIEST!) ⭐

**Prerequisites**: GitHub account (free)

**Steps**:

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Add HalalVest Streamlit app"
   git push origin main
   ```

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
   - Click "New app"
   - Select your GitHub repository
   - Branch: `main`
   - Main file path: `streamlit_app/app.py`
   - Click "Deploy"

3. **Done!** Share the URL with your friend
   - Works on iOS Safari, Android, Desktop
   - Real-time updates
   - Free forever

### 📱 Option 2: Run Locally

**Prerequisites**: Python 3.8+

**Steps**:

1. **Install dependencies**
   ```bash
   cd streamlit_app
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   streamlit run app.py
   ```

3. **Open in browser** - Visit `http://localhost:8501`

### 🔧 Option 3: Deploy to Vercel (Advanced)

See `/backend/` and `/frontend/` directories for React + Node.js setup (coming soon)

## How It Works

### 📊 Dashboard Page
- Overview of halal stocks available
- Your watchlist count
- Quick look at top 15 halal stocks with prices

### 🔍 Stock Analysis Page
- Search any stock symbol
- See full technical analysis (SMA, RSI, MACD, Volume)
- See full fundamental analysis (P/E, D/E, ROE, margins)
- Get buy/sell/hold recommendation with confidence score
- Check halal compliance
- Add to watchlist with one click

### ✅ Halal Screening Page
- Browse pre-screened S&P 500 halal stocks
- Filter stocks by compliance score
- See sector and industry information

### ⭐ Watchlist Page
- See all your saved stocks
- Latest recommendations for each
- Quick view and remove options

### About Page
- Learn how the analysis works
- Important disclaimers
- Data sources and technology

---

## Analysis Methodology

### 1. Halal Stock Screening
- Company sector analysis (excludes prohibited sectors)
- Debt-to-equity ratio check (Islamic principle of avoiding riba)
- Compliance scoring system

**Halal Compliance Criteria**:
- ❌ Excluded sectors: Alcohol, Tobacco, Gambling, Pork, Weapons, Adult, Conventional Finance
- ✅ D/E Ratio: < 1.5 is acceptable
- ✅ Financial health and profitability

### 2. Technical Analysis (50%)
- **SMA (20, 50, 200)**: Identify trends (bullish/bearish/sideways)
- **RSI (14)**: Identify overbought (>70) and oversold (<30) conditions
- **MACD**: Momentum and trend following with histogram
- **Volume Trend**: Confirm price movements strength

### 3. Fundamental Analysis (50%)
- **P/E Ratio**: Valuation (< 15 = undervalued, > 25 = premium)
- **Debt-to-Equity**: Financial health and Islamic compliance
- **ROE**: Return on Equity (profitability efficiency)
- **Profit Margins**: Net, operating, and gross margins

### 4. Recommendation Algorithm
```
Combined Score = (Technical Score × 0.5) + (Fundamental Score × 0.5)

> 65: 🟢 BUY (Strong bullish signals)
55-65: 💹 STRONG HOLD (Positive outlook)
45-55: 〰️ HOLD (Mixed signals)
35-45: ⚠️ WEAK HOLD (Negative outlook)
< 35: 🔴 SELL (Weak bearish signals)

Confidence: How certain the system is (0-100%)
```

### Pre-Screened Halal Stocks (90+)
**Technology**: NVDA, AMD, ORCL, AVGO, ADBE, CRM, INTU, SNPS, MSFT, GOOGL
**Healthcare**: JNJ, UNH, PFE, ABBV, MRK, TMO, LLY, AZN, AMGN, GILD
**Finance**: JPM, BAC, WFC, GS, MS, BLK, SCHW, CME, ICE, MSCI
**Consumer**: AMZN, WMT, HD, MCD, NKE, SBUX, TJX, COST, LOW
**Energy**: XOM, CVX, COP, SLB, MPC, PSX, VLO, FANG, EOG, MUR
**Industrial**: BA, GE, MMM, RTX, HON, CAT, DE, FDX, UPS
**Utilities**: NEE, DUK, SO, D, EXC, AEP, XEL, SRE, WEC
**Real Estate**: PLD, CCI, DLR, EQIX, SPG, O, VICI, STAG, Storage, PSA

And many more! You can also search any stock to analyze it.

### 1. Stock Screening
- Company sector analysis (excludes prohibited sectors)
- Debt-to-equity ratio check (Islamic principle of avoiding riba)
- Compliance with Islamic finance principles

### 2. Technical Analysis
- **SMA (20, 50, 200)**: Identify trends
- **RSI (14)**: Identify overbought/oversold conditions
- **MACD**: Momentum and trend following
- **Volume Trend**: Confirm price movements

### 3. Fundamental Analysis
- **P/E Ratio**: Valuation assessment
- **Debt-to-Equity**: Financial health
- **ROE**: Profitability efficiency
- **Profit Margins**: Operational efficiency

### 4. Recommendation Algorithm
- Combines technical (50%) and fundamental (50%) scores
- **BUY**: Combined score > 65 (bullish signals)
- **SELL**: Combined score < 35 (bearish signals)
- **HOLD**: Combined score 35-65 (mixed signals)
- Includes confidence percentage

## Important Disclaimer

⚠️ **This tool is for EDUCATIONAL purposes only!**

This is NOT financial advice. HalalVest provides analysis and recommendations based on technical and fundamental data, but:
- Always do your own research
- Consult with a financial advisor
- Never invest based solely on this tool
- Stock market involves risk
- Past performance doesn't guarantee future results
- For Islamic finance compliance, consult with a Sharia advisor

## Frequently Asked Questions

**Q: Is this really completely free?**
A: Yes! Streamlit Cloud is free for public apps, Yahoo Finance data is free, and no API keys are required.

**Q: Can my friend use it on his iPhone?**
A: Absolutely! It works perfectly in iOS Safari. You can even add it to home screen for an app-like experience.

**Q: How accurate are the recommendations?**
A: They're based on proven technical and fundamental indicators, but they're a guide, not investment advice. Always do your own research.

**Q: Do I need an API key?**
A: Yes! You need a free Finnhub API key (sign up at https://finnhub.io/register?plan=free). It's free forever with 60 API calls per minute, which is plenty. Store it in `.streamlit/secrets.toml` as `FINNHUB_API_KEY`.

**Q: Can I customize the halal stocks list?**
A: Yes! Edit the `HALAL_STOCKS` list in `streamlit_app/halal_screening.py` to add/remove stocks.

**Q: How often is data updated?**
A: Real-time during market hours. Historical data is updated daily.

**Q: Can I add more indicators?**
A: Yes! The code is modular and easy to extend. Edit `technical_analysis.py` or `fundamental_analysis.py`.

**Q: What if a stock ticker is wrong?**
A: The app will show an error. Make sure you use the correct ticker symbol (e.g., AAPL not Apple).

## Features Roadmap

- [ ] Portfolio tracking
- [ ] Price alerts
- [ ] Email notifications
- [ ] Advanced charting
- [ ] More technical indicators
- [ ] Zakat calculations
- [ ] Multi-language support
- [ ] Performance comparison
- [ ] Historical analysis
- [ ] Community watchlists

## Contributing

We welcome contributions! Areas for improvement:
- More sophisticated ML-based recommendations
- Additional technical indicators
- Real-time alerts and notifications
- More halal stocks database
- Better UI/UX
- Performance optimization
- Bug fixes and improvements

## License

MIT License - feel free to use and modify

## Roadmap

- [ ] Telegram/Discord bot integration
- [ ] Mobile app (iOS/Android)
- [ ] Email alerts
- [ ] Portfolio tracking
- [ ] Risk assessment
- [ ] Zakat calculations
- [ ] Community features

## Support

For issues and feature requests, visit [GitHub Issues](https://github.com/yourrepo/halalvest/issues)

---

Built with ❤️ for Islamic investing community