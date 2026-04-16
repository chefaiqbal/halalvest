import re

with open("/home/amiriqbal/halalvest/streamlit_app/app.py", "r") as f:
    content = f.read()

old_code = """    # Display stocks in columns
    cols = st.columns(5)
    for idx, symbol in enumerate(halal_stocks):
        with cols[idx % 5]:
            if st.button(symbol, key=f"screen_{symbol}"):
                st.session_state.selected_symbol = symbol"""

new_code = """    # Improved Halal Stock Search/Selection UI
    search_col, _ = st.columns([1, 1])
    with search_col:
        search_query = st.text_input("🔍 Search Halal Screened Stocks", "")
        
    filtered_stocks = [s for s in halal_stocks if search_query.upper() in s] if search_query else halal_stocks
    
    # Pagination
    items_per_page = 20
    total_pages = max(1, (len(filtered_stocks) - 1) // items_per_page + 1)
    
    if total_pages > 1:
        page_number = st.select_slider("Page", options=list(range(1, total_pages + 1)), value=1)
    else:
        page_number = 1
        
    start_idx = (page_number - 1) * items_per_page
    end_idx = start_idx + items_per_page
    displayed_stocks = filtered_stocks[start_idx:end_idx]

    st.write(f"Showing **{start_idx + 1}-{min(end_idx, len(filtered_stocks))}** of **{len(filtered_stocks)}** stocks")

    # Display stocks in a clean grid
    cols = st.columns(4)
    for idx, symbol in enumerate(displayed_stocks):
        with cols[idx % 4]:
            if st.button(f"{symbol} 🔍", key=f"screen_{symbol}", use_container_width=True):
                st.session_state.selected_symbol = symbol"""

content = content.replace(old_code, new_code)

with open("/home/amiriqbal/halalvest/streamlit_app/app.py", "w") as f:
    f.write(content)

