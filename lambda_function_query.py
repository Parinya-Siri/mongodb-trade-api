import boto3
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Key

# DynamoDB connection
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AnalysedNewsSentiment')

def lambda_handler(event, context):
    try:
        print("Fetching data from DynamoDB...")
        
        # Fetch all items from DynamoDB
        response = table.scan()
        print("DynamoDB Response:", response)

        # Convert Decimal to float for JSON serialization
        def decimal_default(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Allow CORS for API Gateway
            },
            'body': json.dumps(response['Items'], default=decimal_default)
        }
    except Exception as e:
        print("Error occurred:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
