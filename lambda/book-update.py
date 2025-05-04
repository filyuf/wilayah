import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('books')

def lambda_handler(event, context):
    try:
        # Log the incoming event for debugging
        print("Received event: ", json.dumps(event))
        
        # Extract path parameters (id)
        if 'pathParameters' in event and 'id' in event['pathParameters']:
            id = event['pathParameters']['id']
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing id in path parameters'})
            }
        
        # Check if the event body is already a dict or needs to be loaded from JSON
        if isinstance(event['body'], str):
            body = json.loads(event['body'])  # Load if it's a string
        else:
            body = event['body']  # If it's already a dict, no need to load

        # Ensure 'title' exists in the body
        if 'title' in body:
            title = body['title']
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing title in request body'})
            }
        
        # Update the DynamoDB item (put_item is essentially an upsert operation)
        table.put_item(
            Item={
                'id': id,
                'title': title
            }
        )
        
        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Book with id {id} updated successfully'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # CORS headers if needed
            }
        }
    except Exception as e:
        # Log the exception for debugging
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # CORS headers if needed
            }
        }
