# SentimentStream

**SentimentStream** is a robust, real-time news sentiment analysis platform built for the **MongoDB AI Hackathon**. It leverages AWS services and MongoDB Atlas to transform unstructured news data into structured, actionable insights for trading and decision-making. This project showcases an end-to-end pipeline from data ingestion to visualization on a hosted website.

---

## Inspiration

In the fast-paced trading world, real-time analysis of market sentiment can be a game-changer. SentimentStream was inspired by the challenge of efficiently processing large volumes of news data to deliver sentiment-driven market insights. It aims to provide a scalable, customizable, and insightful tool for traders and analysts alike.

---

## Features

- **Real-time News Fetching**: Continuously collects news articles using the News API.
- **Sentiment Analysis**: Leverages AWS Comprehend to classify articles as positive, negative, neutral, or mixed.
- **Data Storage and Scalability**: Stores raw and analyzed data in MongoDB Atlas and AWS DynamoDB.
- **Web Visualization**: Visualizes results on a hosted website for easy accessibility.
- **Customizable Pipelines**: Flexible components allow swapping or upgrading storage, analysis models, and APIs.

---

## How It Works

### Overview of the Data Pipeline
1. **Data Ingestion**:
   - News articles are fetched from News API using `lambda_function_storing.py`.
   - Articles are stored in MongoDB Atlas with sentiment labels.

2. **Data Analysis**:
   - `lambda_function_analysis.py` processes data stored in MongoDB Atlas.
   - Analyzed data is stored in AWS DynamoDB.

3. **Data Query and Visualization**:
   - `lambda_function_query.py` retrieves data from DynamoDB.
   - Results are visualized in real time on a hosted website at:
     **[SentimentStream Demo](https://sentimentstream-demo.s3.us-east-1.amazonaws.com/index.html)**.

---

## Project Architecture

- **Lambda Functions**:
  1. **`lambda_function_storing.py`**: Fetches and stores news data in MongoDB Atlas.
  2. **`lambda_function_analysis.py`**: Reads data from MongoDB Atlas, performs sentiment analysis, and stores results in DynamoDB.
  3. **`lambda_function_query.py`**: Queries analyzed data from DynamoDB for real-time visualization.

- **AWS Services**:
  - **AWS Comprehend**: Performs sentiment analysis using a pre-trained model.
  - **AWS DynamoDB**: Stores processed data for efficient querying.
  - **AWS S3**: Hosts the visualization website and stores Lambda deployment packages.

- **MongoDB Atlas**: Provides scalable storage for raw news data and intermediate sentiment results.

---

## Deployment

### Prerequisites
Before deploying the Lambda functions, ensure the following prerequisites are met:
- AWS Account with appropriate permissions.
- MongoDB Atlas cluster set up with a connection string.
- News API account with an API key.
- DynamoDB table (`AnalysedNewsSentiment`) created for storing analyzed data.
- S3 bucket created for hosting Lambda deployment packages.

Replace the following placeholders in the Lambda functions with your actual keys and values:
- `AWS_ACCESS_KEY`: Your AWS access key.
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
- `MONGO_CONNECTION_STRING`: Your MongoDB Atlas connection string.
- `NEWS_API_KEY`: Your News API key.
- `TARGET_KEYWORD`: The keyword for the news search (e.g., "Tesla").

### 1. Deploying `lambda_function_storing.py`
- **Purpose**: Fetches data from News API and stores it in MongoDB Atlas.
  
#### Dependencies
This Lambda function has external dependencies (`requests`, `pymongo`, and `boto3`). Follow these steps to package it:
1. **Create a Deployment Package**:
   - Use the `pip` command to install dependencies into a folder:
     ```bash
     mkdir example-lambda-storing
     pip install requests pymongo boto3 -t example-lambda-storing/
     cp lambda_function_storing.py example-lambda-storing/
     ```
2. **Zip the Folder**:
   - Create a `.zip` file for deployment:
     ```bash
     cd example-lambda-storing
     zip -r ../lambda_function_storing.zip .
     cd ..
     ```

#### Deployment Steps
1. **Upload to S3**:
   - Navigate to your S3 bucket in the AWS Console and upload `lambda_function_storing.zip`.
2. **Create Lambda Function**:
   - Go to the **AWS Lambda Console**.
   - Create a new function and choose **Upload from Amazon S3** as the source.
   - Provide the S3 path for your `.zip` file.
3. **Set Environment Variables**:
   - Add the following variables in the Lambda environment:
     - `AWS_ACCESS_KEY`
     - `AWS_SECRET_ACCESS_KEY`
     - `MONGO_CONNECTION_STRING`
     - `NEWS_API_KEY`
     - `TARGET_KEYWORD`
4. **Configure Trigger**:
   - Set up a periodic trigger using **Amazon EventBridge** to run the function at your desired interval (e.g., hourly).

---

### 2. Deploying `lambda_function_analysis.py`
- **Purpose**: Analyzes MongoDB data and stores results in DynamoDB.

#### Dependencies
This Lambda function requires dependencies (`pymongo`, `boto3`). Follow these steps:
1. **Create a Deployment Package**:
   - Install dependencies and prepare the folder:
     ```bash
     mkdir example-lambda-analysis
     pip install pymongo boto3 -t example-lambda-analysis/
     cp lambda_function_analysis.py example-lambda-analysis/
     ```
2. **Zip the Folder**:
   - Create a `.zip` file:
     ```bash
     cd example-lambda-analysis
     zip -r ../lambda_function_analysis.zip .
     cd ..
     ```

#### Deployment Steps
1. **Upload the Package**:
   - Navigate to the **AWS Lambda Console**.
   - Directly upload `lambda_function_analysis.zip` (ensure it’s within the 50MB limit).
2. **Set Environment Variables**:
   - Add the same environment variables as the storing function:
     - `AWS_ACCESS_KEY`
     - `AWS_SECRET_ACCESS_KEY`
     - `MONGO_CONNECTION_STRING`
3. **Configure Execution Role**:
   - Attach a policy to the Lambda execution role allowing access to DynamoDB and MongoDB Atlas.

---

### 3. Deploying `lambda_function_query.py`
- **Purpose**: Queries DynamoDB data for visualization on the website.

#### Deployment Steps
1. **Code Deployment**:
   - This function has no dependencies, so you can directly copy the `lambda_function_query.py` code into the AWS Lambda Console.
2. **API Gateway Setup**:
   - Navigate to **API Gateway Console** and create a new API.
   - **Configure the Route**:
     - Method: `GET`
     - Path: `/mongodbapihackathon-dynamodb-query`
     - Integration: Link it to the `lambda_function_query.py` Lambda function.
   - **Deploy the API**:
     - Deploy the API to a stage (e.g., `prod`).
   - Note the **Invoke URL** provided for the API, such as:
     ```
     https://<api-id>.execute-api.us-east-1.amazonaws.com/prod/mongodbapihackathon-dynamodb-query
     ```

3. **Update Website**:
   - Update the `index.html` file in your S3 bucket to fetch data from the API Gateway’s Invoke URL.

---

### IAM Policies and Permissions
Each Lambda function must have an execution role with the following permissions:
1. **Storing Function**:
   - Access to MongoDB Atlas (configure IP whitelist or VPC peering).
   - Policy Example:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": "s3:*",
           "Resource": "arn:aws:s3:::<your-bucket-name>/*"
         }
       ]
     }
     ```

2. **Analysis Function**:
   - Full access to the `AnalysedNewsSentiment` DynamoDB table.
   - Policy Example:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": "dynamodb:*",
           "Resource": "arn:aws:dynamodb:us-east-1:<account-id>:table/AnalysedNewsSentiment"
         }
       ]
     }
     ```

3. **Query Function**:
   - Read access to the DynamoDB table and allow API Gateway to invoke it.
   - Policy Example:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": "dynamodb:GetItem",
           "Resource": "arn:aws:dynamodb:us-east-1:<account-id>:table/AnalysedNewsSentiment"
         }
       ]
     }
     ```
---

## End-to-End Flow

1. **News API Fetching**:
   - News articles about a target asset (e.g., Tesla) are fetched using keywords.
   - Data is stored in MongoDB Atlas.

2. **Sentiment Analysis**:
   - AWS Comprehend analyzes the articles for sentiment.
   - Analyzed data is stored in DynamoDB, including trends, keyword analysis, and source summaries.

3. **Visualization**:
   - The DynamoDB table is queried using an API Gateway integrated with `lambda_function_query.py`.
   - A website hosted on S3 fetches the API data and visualizes sentiment trends, keyword rankings, and source distributions.

Access the live demo at:
**[SentimentStream Demo](https://sentimentstream-demo.s3.us-east-1.amazonaws.com/index.html)**.

---

## Potential Enhancements

- **Changeable Analysis Methods**:
  - Swap or improve sentiment analysis models with more advanced or custom ML models.

- **Customizable Data Sources**:
  - Integrate additional data sources, such as social media, financial reports, or economic indicators.

- **Scalable Architecture**:
  - Pipeline components are modular, allowing flexibility in storage, analysis, and API endpoints.

- **Historical Insights**:
  - Incorporate historical sentiment trends to provide predictive trading signals.

- **Enhanced Visualization**:
  - Add interactive charts and analytics for deeper insights.

---

## Challenges Faced

1. **Securing MongoDB Atlas**:
   - Configuring IP whitelisting and ensuring secure VPC connectivity.

2. **Dynamic IP Handling**:
   - Solved by using a NAT Gateway to provide static IPs for AWS Lambda.

3. **Resource Constraints**:
   - Optimized Lambda functions to stay within execution time and size limits.

4. **Data Serialization**:
   - Addressed challenges with DynamoDB’s strict data types by converting values to `Decimal`.

---

## Future Plans

- **Advanced Analytics**:
  - Incorporate machine learning to refine sentiment-driven trading signals.

- **Global Expansion**:
  - Scale the platform to cover global assets and data sources.

- **User Dashboard**:
  - Build a user-friendly web interface for traders to explore sentiment trends interactively.
