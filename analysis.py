from pymongo import MongoClient

client = MongoClient("mongodb+srv://joeparinyas:<db_password>@cluster0.lxxzm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.market_data
analysis_collection = db.asset_analysis

def process_data(daily_data):
    processed_data = []
    dates = sorted(daily_data.keys())  # Sort dates to process in order
    previous_close = None

    for date in dates:
        close_price = float(daily_data[date]["4. close"])

        # Calculate daily return if we have a previous close price
        if previous_close:
            daily_return = (close_price - previous_close) / previous_close
        else:
            daily_return = 0.0  # No return for the first day

        # Append processed data
        processed_data.append({
            "date": date,
            "close_price": close_price,
            "daily_return": daily_return
        })
        previous_close = close_price  # Update previous close for the next calculation

    return processed_data

def store_data(symbol, processed_data):
    # Prepare documents for MongoDB with symbol metadata
    documents = [
        {
            "symbol": symbol,
            "date": entry["date"],
            "close_price": entry["close_price"],
            "daily_return": entry["daily_return"]
        }
        for entry in processed_data
    ]
    # Insert documents into MongoDB
    analysis_collection.insert_many(documents)
    print(f"Stored data for {symbol}")


