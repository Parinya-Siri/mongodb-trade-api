import requests

def fetch_daily_data(symbol):
    ALPHA_VANTAGE_API_KEY = "ZTB2XVQAFRUP5YIZ"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" in data:
        daily_data = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(daily_data, orient='index')
        df.columns = ["open", "high", "low", "close", "volume"]
        df = df.astype({"close": "float", "volume": "int"})  # Ensure data types are correct
        df.index = pd.to_datetime(df.index)  # Set the index to date
        return df.sort_index()
    return None
