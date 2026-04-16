import re

with open("/home/amiriqbal/halalvest/streamlit_app/app.py", "r") as f:
    content = f.read()

# Add import for valuation functions
if "from valuation import render_valuation_metrics, render_company_news" not in content:
    content = content.replace("from zakat_calculator import render_zakat_page", "from zakat_calculator import render_zakat_page\nfrom valuation import render_valuation_metrics, render_company_news")

# Insert before Halal Compliance section inside the Analysis layout
old_halal_details = "                    # Halal screening details"
new_halal_details = """                    st.markdown("---")
                    render_valuation_metrics(symbol, tech['current_price'])
                    
                    st.markdown("---")
                    render_company_news(symbol)

                    # Halal screening details"""

content = content.replace(old_halal_details, new_halal_details)

with open("/home/amiriqbal/halalvest/streamlit_app/app.py", "w") as f:
    f.write(content)

