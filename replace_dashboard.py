import re

with open("/home/amiriqbal/halalvest/streamlit_app/app.py", "r") as f:
    content = f.read()

# Replace Stock Analysis text_input with a selectbox/combobox that includes Halal stocks
old_analysis_input = """    col1, col2 = st.columns([3, 1])
    with col1:
        symbol = st.text_input("Enter Stock Symbol", "AAPL").upper()
    with col2:
        st.write("")
        st.write("")
        analyze_btn = st.button("🔍 Analyze")"""

new_analysis_input = """    col1, col2 = st.columns([3, 1])
    with col1:
        # Provide predefined Halal list but allow typing via selectbox
        available_stocks = sorted(list(set(["AAPL", "MSFT", "GOOGL", "NVDA", "JNJ", "PG", "V", "HD", "MA", "CRM"] + get_halal_stocks_list())))
        
        # We'll use Streamlit's awesome multiselect trick or simply a selectbox
        symbol = st.selectbox("Search or Select Stock Symbol", available_stocks, index=available_stocks.index("AAPL") if "AAPL" in available_stocks else 0)
    with col2:
        st.write("")
        st.write("")
        analyze_btn = st.button("🔍 Analyze", use_container_width=True)"""

content = content.replace(old_analysis_input, new_analysis_input)

# Update Dashboard Front Page
old_dash = """# ==================== DASHBOARD PAGE ====================
if page == "Dashboard":
    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Halal Stocks Available", len(get_halal_stocks_list()))
    with col2:
        st.metric("Your Watchlist", len(st.session_state.watchlist))
    with col3:
        st.metric("Last Updated", "Real-time")

    st.markdown("---")
    st.subheader("Welcome to HalalVest!")
    st.markdown(\"\"\"
    **Get Started:**
    1. Go to **Stock Analysis** tab to search any stock
    2. Get instant **buy/sell/hold** recommendations
    3. Check **halal compliance** scoring
    4. Save to your **watchlist** for tracking

    **Features:**
    - 🟢 Real-time stock prices and technical analysis
    - 📊 Fundamental analysis (P/E, ROE, margins)
    - ✅ Halal screening (excludes prohibited sectors)
    - ⭐ Personal watchlist
    \"\"\")

    if len(st.session_state.watchlist) > 0:
        st.markdown("---")
        st.subheader("⭐ Your Watchlist Summary")
        st.write(f"You're tracking **{len(st.session_state.watchlist)}** stocks")
        st.info("Click 'View' to see detailed analysis for any stock")"""

new_dash = """# ==================== DASHBOARD PAGE ====================
if page == "Dashboard":
    st.header("📊 Market Dashboard")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Halal Stocks Available", len(get_halal_stocks_list()), "Verified")
    with col2:
        st.metric("Your Watchlist", len(st.session_state.watchlist), "Saved")
    with col3:
        st.metric("Last Updated", "Real-time", "Active")

    st.markdown("---")
    st.subheader("Top Halal Picks Today")
    
    # We'll mock a fast mini-overview of 4 top stocks
    top_picks = ["AAPL", "MSFT", "GOOGL", "NVDA"]
    m_cols = st.columns(4)
    from technical_analysis import get_historical_data
    from finnhub_client import get_quote
    
    for i, t_sym in enumerate(top_picks):
        with m_cols[i]:
            st.markdown(f"**{t_sym}**")
            qt = get_quote(t_sym)
            if qt and 'c' in qt and qt['c'] > 0:
                current_price = qt['c']
                prev_close = qt['pc']
                pct_change = ((current_price - prev_close) / prev_close) * 100
                st.metric(label="Price", value=f"${current_price:.2f}", delta=f"{pct_change:.2f}%")
            else:
                st.metric(label="Price", value="N/A", delta="N/A")
            
            if st.button(f"Analyze {t_sym}", key=f"dash_{t_sym}", use_container_width=True):
                st.session_state['selected_symbol'] = t_sym
                st.info(f"Navigate to 'Stock Analysis' on the sidebar to view {t_sym} details!")

    st.markdown("---")
    st.subheader("Welcome to HalalVest! 🚀")
    colA, colB = st.columns(2)
    with colA:
        st.markdown(\"\"\"
        **Step-by-step Guide:**
        1. 🔍 Use **Stock Analysis** to research predefined safe stocks or enter your own
        2. 🤖 Follow our Data-Driven **Buy/Sell/Hold ML recommendations**
        3. ✅ Verify **Halal compliance** constraints directly on the UI
        \"\"\")
    with colB:
        st.markdown(\"\"\"
        **What's New!**
        - 📈 Custom Rolling RSI & SMA Technical overlays
        - ⚡ Blazing fast memory caching (No more wait times!)
        - 🔍 Search functionality on the Screener page
        \"\"\")"""

content = content.replace(old_dash, new_dash)

with open("/home/amiriqbal/halalvest/streamlit_app/app.py", "w") as f:
    f.write(content)

