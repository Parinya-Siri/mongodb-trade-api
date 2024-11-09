import alphavantage, analysis

stocks = {"AAPL"}

for stock in stocks:
    daily_data = alphavantage.fetch_daily_data(stock)
    if daily_data:
        processed_data = analysis.process_data(daily_data)
        analysis.store_data(stock, processed_data)