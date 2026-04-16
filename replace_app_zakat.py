import re

with open("/home/amiriqbal/halalvest/streamlit_app/app.py", "r") as f:
    content = f.read()

# Add import for zakat calculator
if "from zakat_calculator import render_zakat_page" not in content:
    content = content.replace("import logging", "import logging\nfrom zakat_calculator import render_zakat_page")

# Update side bar menu list
old_radio = '["Dashboard", "Stock Analysis", "Charts & Comparison", "Portfolio Performance", "Halal Screening", "My Watchlist", "About"])'
new_radio = '["Dashboard", "Stock Analysis", "Charts & Comparison", "Portfolio Performance", "Halal Screening", "My Watchlist", "Zakat & Purification", "About"])'
content = content.replace(old_radio, new_radio)

# Insert the routing for Zakat page right before About page
old_about = 'elif page == "About":'
new_zakat_and_about = '''elif page == "Zakat & Purification":
    render_zakat_page()

# ==================== ABOUT PAGE ====================
elif page == "About":'''
content = content.replace(old_about, new_zakat_and_about)

with open("/home/amiriqbal/halalvest/streamlit_app/app.py", "w") as f:
    f.write(content)

