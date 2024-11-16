from pymongo import MongoClient
import boto3
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import re

# MongoDB connection
your_mongo_connection_string = ""
client = MongoClient(your_mongo_connection_string)
db = client.market_data

# DynamoDB connection
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AnalysedNewsSentiment')

def lambda_handler(event, context):
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)

    # Fetch sentiment data from MongoDB
    sentiment_data = list(db.news_sentiment.find({
        "timestamp": {"$gte": yesterday.isoformat(), "$lt": now.isoformat()}
    }))

    # Initialize aggregations
    sentiment_counts = {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
    sentiment_trends = defaultdict(lambda: {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0, "count": 0})
    source_counts = Counter()
    text_data = []

    # Process each document
    for doc in sentiment_data:
        # Sentiment distribution
        sentiment_counts[doc['sentiment']] += 1

        # Sentiment trends (group by date)
        date = doc['timestamp'][:10]  # Extract YYYY-MM-DD
        sentiment_trends[date][doc['sentiment']] += 1
        sentiment_trends[date]["count"] += 1

        # Source analysis
        source_counts[doc['source']] += 1

        # Collect text data for keyword analysis
        text_data.append(doc.get('title', '') + " " + doc.get('description', ''))

    # Prepare sentiment trends for DynamoDB
    trends = []
    for date, counts in sentiment_trends.items():
        trends.append({
            "date": date,
            "positive": counts["POSITIVE"],
            "neutral": counts["NEUTRAL"],
            "negative": counts["NEGATIVE"],
            "total": counts["count"]
        })

    # Keyword analysis
    text = " ".join(text_data)
    words = re.findall(r'\b\w+\b', text.lower())  # Split text into words
    stopwords = set(["the", "and", "of", "to", "a", "is", "in", "for", "on"])
    keyword_counts = Counter(word for word in words if word not in stopwords)
    top_keywords = dict(keyword_counts.most_common(10))

    # Sentiment vs Volume
    sentiment_vs_volume = []
    for date, counts in sentiment_trends.items():
        sentiment_vs_volume.append({
            "date": date,
            "volume": counts["count"],
            "average_positive_score": counts["POSITIVE"] / counts["count"] if counts["count"] > 0 else 0
        })

    # Store all results in DynamoDB
    table.put_item(
        Item={
            'date': now.date().isoformat(),
            'asset': 'Tesla',
            'sentiment_distribution': sentiment_counts,
            'sentiment_trends': trends,
            'top_sources': dict(source_counts.most_common(10)),
            'top_keywords': top_keywords,
            'sentiment_vs_volume': sentiment_vs_volume,
            'updated_at': now.isoformat()
        }
    )

    return {"status": "success", "message": "Data analyzed and stored in DynamoDB"}
