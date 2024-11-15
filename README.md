# SentimentStream

**SentimentStream** is a real-time news sentiment analysis platform built for the **MongoDB AI Hackathon**. The project leverages AWS services and MongoDB Atlas to analyze news sentiment for generating actionable trading insights.

## Inspiration

In the fast-paced world of trading, staying ahead requires analyzing vast amounts of data, especially real-time news. SentimentStream was inspired by the challenge of turning unstructured news data into structured, actionable insights using AI. This project combines sentiment analysis with scalable data processing to empower traders with sentiment-driven market signals.

## Features

- **Real-time news fetching**: Continuously collects news articles from sources like News API.
- **Sentiment analysis**: Uses AWS Comprehend to classify articles as positive, negative, or neutral.
- **Scalable storage**: Stores analyzed data in MongoDB Atlas for long-term use and retrieval.
- **Automated workflow**: Powered by AWS Lambda for seamless ingestion and analysis.

## How It Works

1. **Data Ingestion**: News articles related to specific stocks or keywords are fetched using the News API.
2. **Sentiment Analysis**: AWS Comprehend processes the article text to determine sentiment and confidence scores.
3. **Storage**: Results are stored in MongoDB Atlas for further analysis and visualization.
4. **Automation**: AWS Lambda automates the entire process, running periodically to ensure up-to-date data.

## Project Architecture

- **AWS Lambda**: Automates data ingestion and processing workflows.
- **AWS Comprehend**: Performs sentiment analysis on news articles.
- **MongoDB Atlas**: Stores the sentiment data for visualization and trading signal generation.
- **S3**: Used to host Lambda deployment packages for efficient function updates.

## Usage

### 1. Install Required Libraries
Make sure you have Python installed. Then, install the required dependencies:
    ```bash
    pip install requests boto3 pymongo

### 2. Set Up the Example Lambda Function

1. Navigate to the `example-lambda-folder` provided in the repository.
2. Edit the placeholder keys in the `lambda_function.py` file:
   - Replace the following placeholders with your actual keys and values:
     - `AWS_ACCESS_KEY`: Your AWS access key.
     - `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
     - `MONGO_CONNECTION_STRING`: Your MongoDB Atlas connection string.
     - `NEWS_API_KEY`: Your News API key.
     - `TARGET_KEYWORD`: The keyword for the news search (e.g., "Tesla").
3. Zip the contents of the folder
4. Upload the .zip file to an S3 bucket in AWS.

### 3. Deploy the Lambda Function
1. Go to the AWS Lambda console and create a new function.
2. Choose Upload from Amazon S3 and provide the S3 path to your deployment package.
3. Configure environment variables and set up a CloudWatch event to trigger the function periodically.

### 4. Run and Monitor
Test the Lambda function and monitor the logs in AWS CloudWatch to ensure it’s working correctly.

## Challenges Faced

- **SSL Handshake Issues**: Setting up a secure connection between AWS Lambda and MongoDB Atlas required configuring VPCs and NAT Gateways.
- **Handling Dynamic IPs**: AWS Lambda's dynamic IPs posed challenges for whitelisting in MongoDB Atlas, solved by routing traffic through a NAT Gateway with a static IP.
- **Execution Limits**: Balancing Lambda timeout and memory settings to accommodate the processing of large news datasets and sentiment analysis.

## Future Plans

- **Historical Analysis**: Integrate historical sentiment trends for more comprehensive trading signals.
- **Broader Data Sources**: Include social media sentiment and economic indicators.
- **Advanced Signals**: Improve trading signal algorithms with machine learning for enhanced predictions.
