import json
import boto3

# Initialising the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('books')  # The name of your DynamoDB table

def lambda_handler(event, context):
    try:
        params = {
            'TableName': 'books'
        }
        
        # Utilising the scan method to get all items in the table
        response = table.scan(**params)
        
        data = response['Items']
        
        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }
    except Exception as e:
        return {
            'statusCode': 500
        }
