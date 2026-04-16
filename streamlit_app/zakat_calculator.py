import streamlit as st

def render_zakat_page():
    st.header("🕌 Zakat & Dividend Purification")
    
    st.markdown("""
    This tool helps you calculate your annual **Zakat** obligation and determine how much of your 
    dividend income needs **Purification** due to non-compliant sources (e.g., fractional interest).
    """)

    tab1, tab2 = st.tabs(["Zakat Calculator", "Dividend Purification"])

    with tab1:
        st.subheader("Calculate Your Zakat")
        st.markdown("Zakat is obligatory charity (2.5%) on wealth held for over one full lunar year.")
        
        col1, col2 = st.columns(2)
        with col1:
            stock_value = st.number_input("Total Stock Portfolio Value ($)", min_value=0.0, value=0.0, step=100.0, help="Current market value of your shares.")
            cash_value = st.number_input("Cash & Savings ($)", min_value=0.0, value=0.0, step=100.0, help="Liquid cash held for over a year.")
        with col2:
            gold_value = st.number_input("Gold & Silver Value ($)", min_value=0.0, value=0.0, step=100.0, help="Value of physical gold/silver.")
            other_assets = st.number_input("Other Zakat-eligible Assets ($)", min_value=0.0, value=0.0, step=100.0, help="Business inventory, properties bought to sell, etc.")
        
        total_wealth = stock_value + cash_value + gold_value + other_assets
        
        # Nisab estimation (85 grams of gold, usually around $6,500)
        nisab_threshold = 6500.0
        
        st.write("---")
        colA, colB = st.columns(2)
        with colA:
            st.metric("Total Zakat-Eligible Wealth", f"${total_wealth:,.2f}")
            st.info(f"Current estimated Nisab (threshold): ~${nisab_threshold:,.2f}")
            
        with colB:
            if total_wealth >= nisab_threshold:
                zakat_due = total_wealth * 0.025
                st.success(f"### Zakat Due: ${zakat_due:,.2f}")
                st.markdown("*(2.5% of total wealth)*")
            elif total_wealth > 0:
                st.warning("### Zakat Due: $0.00")
                st.markdown("*Your wealth is currently below the Nisab threshold.*")
            else:
                st.write("### Zakat Due: $0.00")
                
    with tab2:
        st.subheader("Dividend Purification")
        st.markdown("""
        Even Shariah-compliant companies occasionally park money in interest-bearing accounts.
        Scholars advise calculating the proportion of non-compliant income and donating it.
        **The general conservative rule of thumb without doing specific accounting is 5% of dividends.**
        """)
        
        div_col1, div_col2 = st.columns([2, 1])
        with div_col1:
            total_dividends = st.number_input("Total Annual Dividends Received ($)", min_value=0.0, value=0.0, step=10.0)
        with div_col2:
            purification_rate = st.slider("Purification Rate (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.5, help="Standard safe assumption is ~5%.")
        
        amount_to_purify = total_dividends * (purification_rate / 100)
        st.write("---")
        if amount_to_purify > 0:
            st.error(f"### Amount to Purify (Donate): ${amount_to_purify:,.2f}")
            st.markdown("💡 *Note: Give this amount to the poor without expecting religious reward (thawab) for charity, as it is just disposing of impermissible money.*")
        else:
            st.write("### Amount to Purify (Donate): $0.00")

