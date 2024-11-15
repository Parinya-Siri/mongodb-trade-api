from pymongo import MongoClient
import requests
import boto3
from datetime import datetime

# All keys here
my_mongo_connection_string = ""
my_aws_access_key = ""
my_aws_secret_access_key = ""
my_news_api_key = ""
my_news_target = ""

# MongoDB connection setup
client = MongoClient(my_mongo_connection_string)
db = client.market_data
news_sentiment_collection = db.news_sentiment

# AWS Comprehend client setup
comprehend = boto3.client(
    "comprehend",
    aws_access_key_id=my_aws_access_key,
    aws_secret_access_key=my_aws_secret_access_key,
    region_name="us-east-1"
)

# Function to fetch news data from News API
def fetch_news(query, api_key):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles']
    return []

# Function to analyze sentiment using AWS Comprehend
def analyze_sentiment(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return response['Sentiment'], response['SentimentScore']

# Get the latest timestamp from MongoDB to only fetch new articles
def get_latest_timestamp(symbol):
    latest_article = news_sentiment_collection.find_one(
        {"asset": symbol},
        sort=[("timestamp", -1)]  # Sort by timestamp descending
    )
    if latest_article:
        return datetime.strptime(latest_article["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
    else:
        return None

# Process and store only new articles in MongoDB
def process_and_store_new_articles(news_data, symbol):
    latest_timestamp = get_latest_timestamp(symbol)
    
    for article in news_data:
        # Parse article timestamp
        article_timestamp = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
        
        # Only proceed if article is new or if MongoDB is empty (latest_timestamp is None)
        if latest_timestamp is None or article_timestamp > latest_timestamp:
            if 'description' in article and article['description']:
                sentiment, sentiment_score = analyze_sentiment(article['description'])
                sentiment_doc = {
                    "asset": symbol,
                    "timestamp": article['publishedAt'],
                    "title": article['title'],
                    "description": article['description'],
                    "sentiment": sentiment,
                    "sentiment_score": sentiment_score,
                    "source": article['source']['name']
                }
                news_sentiment_collection.insert_one(sentiment_doc)
                print(f"Inserted document for article: {article['title']}")
            else:
                print("Skipping article with missing or empty description:", article.get('title'))
        else:
            print("Article already exists in the database, skipping:", article.get('title'))

# Main function to be triggered periodically
def lambda_handler(event, context):
    # Fetch latest news data
    news_data = fetch_news(my_news_target, my_news_api_key)
    # Process and store only new articles
    process_and_store_new_articles(news_data, my_news_target)

# Run the main function (for testing or direct execution)
if __name__ == "__main__":
    news_data = fetch_news(my_news_target, my_news_api_key)
    process_and_store_new_articles(news_data, my_news_target)
